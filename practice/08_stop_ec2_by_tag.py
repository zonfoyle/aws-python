"""
Stop EC2 instances based on a tag
"""

# Import boto3
import boto3


# -------------------------------
# Create EC2 Client
# -------------------------------

ec2 = boto3.client('ec2', region_name='us-east-1')


# -------------------------------
# Define Tag Filter
# -------------------------------

# This will find instances with this tag
tag_key = "Environment"
tag_value = "dev"


# -------------------------------
# Find Matching Instances
# -------------------------------

response = ec2.describe_instances(
    Filters=[
        {
            'Name': f'tag:{tag_key}',
            'Values': [tag_value]
        }
    ]
)


# -------------------------------
# Collect Instance IDs
# -------------------------------

instance_ids = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_ids.append(instance['InstanceId'])


# -------------------------------
# Stop Instances
# -------------------------------

if instance_ids:
    ec2.stop_instances(InstanceIds=instance_ids)
    print("Stopping instances:", instance_ids)
else:
    print("No instances found with the specified tag.")