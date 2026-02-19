"""
AWS S3 CRUD Automation Script
Author: Zonique Foyle

Purpose:
Demonstrates how to automate S3 bucket creation using Python + Boto3.

Concepts covered:
- AWS SDK authentication
- Region-aware bucket deployment
- Globally unique naming strategy
- Exception handling with botocore
"""

# Import the boto3 library
import boto3
import time
from botocore.exceptions import ClientError

# Instantiate a boto3 S3 client
# (client is preferred over resource for real AWS automation work)
session = boto3.session.Session()
region = session.region_name or "us-east-1"
s3 = session.client("s3", region_name=region)

# Name the bucket (must be globally unique in AWS)
bucket_name = f"zonique-crud-{int(time.time())}"
print("DEBUG bucket_name =", bucket_name)
print("DEBUG region =", region)

# Check if bucket exists
# Create the bucket if it does NOT exist
# NOTE:
# - S3 bucket names are global across ALL AWS users
# - Timestamp ensures uniqueness
# - Region matters when creating buckets

try:
    print(f"'{bucket_name}' bucket does not exist. Creating now...")

    # us-east-1 requires a different create format
    if region == "us-east-1":
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region}
        )

    print(f"'{bucket_name}' bucket has been created.")

except ClientError as e:
    error_code = e.response["Error"]["Code"]
    error_message = e.response["Error"]["Message"]
    print(f"Error creating bucket: {error_code} - {error_message}")




