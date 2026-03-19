"""
Launch an EC2 instance inside a subnet.

Architecture

Internet
↓
Internet Gateway
↓
Route Table
↓
Subnet
↓
EC2 Instance
"""

# Import boto3 so Python can communicate with AWS
import boto3


# -------------------------------
# Create EC2 Client
# -------------------------------

ec2 = boto3.client('ec2', region_name='us-east-1')


# -------------------------------
# Required Resource IDs
# -------------------------------

# Replace these with your actual resource IDs

subnet_id = "subnet-xxxxxxxx"
security_group_id = "sg-xxxxxxxx"
key_name = "ec2-practice-key"


# -------------------------------
# Launch EC2 Instance
# -------------------------------

response = ec2.run_instances(

    # Amazon Linux 2023 AMI
    ImageId='ami-0c02fb55956c7d316',

    # Instance type
    InstanceType='t3.micro',

    # SSH key pair
    KeyName=key_name,

    # Launch in the subnet you created
    SubnetId=subnet_id,

    # Attach security group
    SecurityGroupIds=[security_group_id],

    # Minimum and maximum instances
    MinCount=1,
    MaxCount=1,

    # Assign public IP automatically
    NetworkInterfaces=[
        {
            'SubnetId': subnet_id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [security_group_id]
        }
    ]
)


# -------------------------------
# Extract Instance ID
# -------------------------------

instance_id = response['Instances'][0]['InstanceId']

print("EC2 Instance launched:", instance_id)


# -------------------------------
# Add Name Tag
# -------------------------------

ec2.create_tags(
    Resources=[instance_id],
    Tags=[
        {
            "Key": "Name",
            "Value": "boto3-ec2-instance"
        }
    ]
)

print("EC2 instance tagged successfully.")
