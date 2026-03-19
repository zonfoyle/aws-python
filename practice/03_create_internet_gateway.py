"""
Create and attach an Internet Gateway to a VPC.

Architecture

Internet
↓
Internet Gateway
↓
VPC
↓
Subnets
"""

# Import boto3 so Python can communicate with AWS
import boto3


# -------------------------------
# Create EC2 Client
# -------------------------------

# VPC networking is handled through the EC2 API
ec2 = boto3.client('ec2', region_name='us-east-1')


# -------------------------------
# VPC ID
# -------------------------------

# Replace with your existing VPC ID
vpc_id = "vpc-xxxxxxxx"

# -------------------------------
# Create Internet Gateway
# -------------------------------

# Internet Gateway allows resources inside a VPC
# to communicate with the public internet

response = ec2.create_internet_gateway()

# Extract Internet Gateway ID
igw_id = response['InternetGateway']['InternetGatewayId']

print("Internet Gateway created:", igw_id)


# -------------------------------
# Attach Internet Gateway to VPC
# -------------------------------

# An Internet Gateway must be attached to a VPC
# before it can route traffic

ec2.attach_internet_gateway(
    InternetGatewayId=igw_id,
    VpcId=vpc_id
)

print("Internet Gateway attached to VPC.")

# -------------------------------
# Add Name Tag
# -------------------------------

# Tags make resources easier to identify in the AWS console

ec2.create_tags(
    Resources=[igw_id],
    Tags=[
        {
            "Key": "Name",
            "Value": "boto3-internet-gateway"
        }
    ]
)

print("Internet Gateway configured successfully.")
