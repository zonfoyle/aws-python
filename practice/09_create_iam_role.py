"""
Create an IAM Role using boto3

Goal:
Create an IAM role programmatically with Python and boto3.

This script teaches:
1. How to connect to AWS IAM with boto3
2. How to create a trust policy
3. How to create an IAM role
4. How to attach a managed permission policy

Important concept:
An IAM role usually needs 2 things:

1. Trust Policy
   - Defines WHO can assume the role
   - Example: EC2 can assume the role

2. Permission Policy
   - Defines WHAT the role can do after it is assumed
   - Example: Read from S3
"""

# Import boto3 so Python can communicate with AWS
import boto3

# Import json so we can convert Python dictionaries
# into JSON format for AWS
import json


# -----------------------------------
# Create IAM Client
# -----------------------------------

# IAM is a global AWS service, so region is not required here
iam = boto3.client("iam")


# -----------------------------------
# Define Role Name
# -----------------------------------

role_name = "EC2S3ReadRole"


# -----------------------------------
# Define Trust Policy
# -----------------------------------

# Trust Policy = WHO can assume the role
# In this example, EC2 instances are allowed to assume this role

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}


# -----------------------------------
# Create IAM Role
# -----------------------------------

response = iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(trust_policy),
    Description="IAM role for EC2 to read from S3"
)

print("IAM Role created:", response["Role"]["RoleName"])


# -----------------------------------
# Attach Managed Permission Policy
# -----------------------------------

# Permission Policy = WHAT the role can do
# This AWS managed policy allows read-only access to S3

iam.attach_role_policy(
    RoleName=role_name,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
)

print("Managed policy attached successfully.")


# -----------------------------------
# Done
# -----------------------------------

print("IAM role setup complete.")