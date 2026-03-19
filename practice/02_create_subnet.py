"""
Create a subnet inside an existing VPC.

Architecture
VPC (10.0.0.0/16)
↓
Subnet (10.0.1.0/24)
"""

# Import boto3 so Python can communicate with AWS
import boto3


# Create an EC2 client (VPC networking is managed through the EC2 service)
ec2 = boto3.client('ec2', region_name='us-east-1')

# -------------------------------
# VPC ID
# -------------------------------

# The VPC where the subnet will be created
# Replace this with your actual VPC ID
vpc_id = "vpc-xxxxxxxx"


# -------------------------------
# Create Subnet
# -------------------------------

# A subnet represents a smaller network segment inside a VPC
# CIDR block 10.0.1.0/24 gives us 256 private IP addresses

response = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24'
)


# -------------------------------
# Extract Subnet ID
# -------------------------------

# AWS returns a response object containing details about the subnet
# We extract the subnet ID so we can reference it later

subnet_id = response['Subnet']['SubnetId']

print("Subnet created:", subnet_id)


# -------------------------------
# Enable Auto Assign Public IP
# -------------------------------

# This allows EC2 instances launched in this subnet
# to automatically receive a public IP address

ec2.modify_subnet_attribute(
    SubnetId=subnet_id,
    MapPublicIpOnLaunch={'Value': True}
)

# -------------------------------
# Add Name Tag
# -------------------------------

# Tags make resources easier to identify in the AWS console

ec2.create_tags(
    Resources=[subnet_id],
    Tags=[
        {
            "Key": "Name",
            "Value": "boto3-public-subnet"
        }
    ]
)

print("Subnet configured successfully.")