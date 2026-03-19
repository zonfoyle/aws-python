"""
Create a Route Table in a VPC and add a route to an Internet Gateway
"""

# Import boto3 so Python can communicate with AWS
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')

# Replace with your VPC ID
vpc_id = "vpc-xxxxxxxx"

# Replace with your Internet Gateway ID
igw_id = "igw-xxxxxxxx"


# ---------------------------------------------------
# Create the route table inside the VPC
# ---------------------------------------------------

response = ec2.create_route_table(
    VpcId=vpc_id
)

# Extract the route table ID
route_table_id = response['RouteTable']['RouteTableId']

print("Route table created:", route_table_id)


# ---------------------------------------------------
# Create a route to the internet
# ---------------------------------------------------

ec2.create_route(
    RouteTableId=route_table_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw_id
)

print("Internet route added.")


# ---------------------------------------------------
# Tag the route table so it appears nicely in console
# ---------------------------------------------------

ec2.create_tags(
    Resources=[route_table_id],
    Tags=[{"Key": "Name", "Value": "boto3-route-table"}]
)

print("Route table setup complete.")