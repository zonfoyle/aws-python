"""
Creates a basic VPC.

Architecture:
VPC (10.0.0.0/16)
DNS support enabled
DNS hostnames enabled
Tagged for identification
"""
# Import boto3 so Python can communicate with AWS
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')

# Create the VPC
response = ec2.create_vpc(CidrBlock='10.0.0.0/16')

# Extract the VPC ID
vpc_id = response['Vpc']['VpcId']

print("VPC created:", vpc_id)


"""
Additional steps commonly used after creating a VPC
"""

# Wait until the VPC is fully available
waiter = ec2.get_waiter('vpc_available')
waiter.wait(VpcIds=[vpc_id])

# Enable DNS support
ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsSupport={'Value': True}
)

# Enable DNS hostnames
ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsHostnames={'Value': True}
)

# Add Name tag
ec2.create_tags(
    Resources=[vpc_id],
    Tags=[{"Key": "Name", "Value": "boto3-practice-vpc"}]
)

print("VPC setup complete.")
