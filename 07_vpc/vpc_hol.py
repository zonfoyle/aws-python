"""
Create a simple public VPC setup:
- VPC (10.0.0.0/16)
- Internet Gateway attached to VPC
- Public route table with 0.0.0.0/0 -> IGW
- 3 public subnets across first 3 AZs (or fewer if region has fewer)
- Route table association for each subnet
- Tags on everything

Run it multiple times safely (it won't keep creating duplicates).
"""

import boto3
from botocore.exceptions import ClientError


VPC_NAME = "vpc-hol"
IGW_NAME = "ig-vpc-hol"
RT_NAME = "rt-public-vpc-hol"
SUBNET_NAMES = ["public-subnet-1", "public-subnet-2", "public-subnet-3"]
SUBNET_CIDRS = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]


def get_ec2(region=None):
    session = boto3.session.Session()
    region_name = region or session.region_name or "us-east-1"
    return session.client("ec2", region_name=region_name), region_name


def tag_resource(ec2, resource_id, name):
    ec2.create_tags(Resources=[resource_id], Tags=[{"Key": "Name", "Value": name}])


def find_vpc_by_name(ec2, name):
    resp = ec2.describe_vpcs(Filters=[{"Name": "tag:Name", "Values": [name]}])
    vpcs = resp.get("Vpcs", [])
    return vpcs[0]["VpcId"] if vpcs else None


def ensure_vpc(ec2, name, cidr_block):
    vpc_id = find_vpc_by_name(ec2, name)
    if vpc_id:
        print(f"VPC exists: {name} ({vpc_id})")
        return vpc_id

    resp = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = resp["Vpc"]["VpcId"]

    # Good default for many setups
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})

    tag_resource(ec2, vpc_id, name)
    print(f"Created VPC: {name} ({vpc_id})")
    return vpc_id


def find_igw_by_name(ec2, name):
    resp = ec2.describe_internet_gateways(
        Filters=[{"Name": "tag:Name", "Values": [name]}]
    )
    igws = resp.get("InternetGateways", [])
    return igws[0] if igws else None


def ensure_igw(ec2, vpc_id, name):
    igw = find_igw_by_name(ec2, name)

    if igw:
        igw_id = igw["InternetGatewayId"]
        attached_vpcs = [a["VpcId"] for a in igw.get("Attachments", [])]
        if vpc_id not in attached_vpcs:
            ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
            print(f"Attached IGW to VPC: {name} ({igw_id}) -> {vpc_id}")
        else:
            print(f"IGW already attached: {name} ({igw_id})")
        return igw_id

    resp = ec2.create_internet_gateway()
    igw_id = resp["InternetGateway"]["InternetGatewayId"]
    tag_resource(ec2, igw_id, name)
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
    print(f"Created + attached IGW: {name} ({igw_id})")
    return igw_id


def find_route_table_by_name(ec2, vpc_id, name):
    resp = ec2.describe_route_tables(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]},
            {"Name": "tag:Name", "Values": [name]},
        ]
    )
    rts = resp.get("RouteTables", [])
    return rts[0] if rts else None


def ensure_public_route_table(ec2, vpc_id, igw_id, name):
    rt = find_route_table_by_name(ec2, vpc_id, name)

    if rt:
        rt_id = rt["RouteTableId"]
        print(f"Route table exists: {name} ({rt_id})")
    else:
        resp = ec2.create_route_table(VpcId=vpc_id)
        rt_id = resp["RouteTable"]["RouteTableId"]
        tag_resource(ec2, rt_id, name)
        print(f"Created route table: {name} ({rt_id})")

    # Ensure default route exists (ignore if already there)
    try:
        ec2.create_route(
            RouteTableId=rt_id,
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=igw_id,
        )
        print(f"Added route 0.0.0.0/0 -> IGW on {rt_id}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("RouteAlreadyExists", "InvalidRoute.Duplicate"):
            pass
        else:
            raise

    return rt_id


def list_azs(ec2):
    resp = ec2.describe_availability_zones(
        Filters=[{"Name": "state", "Values": ["available"]}]
    )
    return [az["ZoneName"] for az in resp.get("AvailabilityZones", [])]


def find_subnet_by_name(ec2, vpc_id, name):
    resp = ec2.describe_subnets(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]},
            {"Name": "tag:Name", "Values": [name]},
        ]
    )
    subnets = resp.get("Subnets", [])
    return subnets[0]["SubnetId"] if subnets else None


def ensure_subnet(ec2, vpc_id, name, cidr_block, az):
    subnet_id = find_subnet_by_name(ec2, vpc_id, name)
    if subnet_id:
        print(f"Subnet exists: {name} ({subnet_id})")
        return subnet_id

    resp = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block, AvailabilityZone=az)
    subnet_id = resp["Subnet"]["SubnetId"]
    tag_resource(ec2, subnet_id, name)

    # Public subnet behavior
    ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={"Value": True})

    print(f"Created subnet: {name} ({subnet_id}) in {az} [{cidr_block}]")
    return subnet_id


def ensure_route_table_association(ec2, rt_id, subnet_id):
    rt = ec2.describe_route_tables(RouteTableIds=[rt_id])["RouteTables"][0]
    associations = rt.get("Associations", [])

    for assoc in associations:
        if assoc.get("SubnetId") == subnet_id:
            return  # already associated

    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_id)
    print(f"Associated route table {rt_id} -> subnet {subnet_id}")


def main():
    ec2, region = get_ec2()
    print(f"Region: {region}")

    vpc_id = ensure_vpc(ec2, VPC_NAME, "10.0.0.0/16")
    igw_id = ensure_igw(ec2, vpc_id, IGW_NAME)
    rt_id = ensure_public_route_table(ec2, vpc_id, igw_id, RT_NAME)

    azs = list_azs(ec2)
    if not azs:
        raise RuntimeError("No available AZs found in this region.")

    # Use up to first 3 AZs (depending on region)
    target_azs = azs[:3]

    subnet_ids = []
    for i, az in enumerate(target_azs):
        name = SUBNET_NAMES[i]
        cidr = SUBNET_CIDRS[i]
        subnet_id = ensure_subnet(ec2, vpc_id, name, cidr, az)
        subnet_ids.append(subnet_id)
        ensure_route_table_association(ec2, rt_id, subnet_id)

    print("\nDone.")
    print(f"VPC: {vpc_id}")
    print(f"IGW: {igw_id}")
    print(f"Route Table: {rt_id}")
    print(f"Subnets: {', '.join(subnet_ids)}")


if __name__ == "__main__":
    main()