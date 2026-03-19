"""
Filter EC2 instances by state (running)
"""

import boto3


# -------------------------------
# Create EC2 Client
# -------------------------------

ec2 = boto3.client('ec2', region_name='us-east-1')


# -------------------------------
# Filter Running Instances
# -------------------------------

response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
)


# -------------------------------
# Print Results
# -------------------------------

for reservation in response['Reservations']:
    for instance in reservation['Instances']:

        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']

        print("Running Instance:", instance_id)
        print("Type:", instance_type)
        print("State:", state)
        print("---------------------------")