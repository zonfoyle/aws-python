"""
List all EC2 instances in the AWS account
"""

# Import boto3 so Python can communicate with AWS
import boto3


# -------------------------------
# Create EC2 Client
# -------------------------------

ec2 = boto3.client('ec2', region_name='us-east-1')


# -------------------------------
# Get EC2 Instances
# -------------------------------

response = ec2.describe_instances()


# -------------------------------
# Loop Through Instances
# -------------------------------

for reservation in response['Reservations']:
    for instance in reservation['Instances']:

        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']

        print("Instance ID:", instance_id)
        print("Instance Type:", instance_type)
        print("State:", state)
        print("---------------------------")