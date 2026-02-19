"""
AWS S3 Bucket Create Script
Author: Zonique Foyle

Purpose:
Demonstrates how to create an S3 bucket using Python + Boto3.

Concepts covered:
- AWS SDK authentication via default credential chain
- Region-aware bucket creation (us-east-1 special case)
- Globally unique naming strategy using timestamps
- Exception handling with botocore
"""

from __future__ import annotations

import logging
import time

import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name: str, region: str) -> None:
    """Create an S3 bucket in the specified region."""
    session = boto3.session.Session()
    s3 = session.client("s3", region_name=region)

    logging.info("Bucket name: %s", bucket_name)
    logging.info("Region: %s", region)

    try:
        # us-east-1 requires a different create format
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )

        logging.info("Bucket created: %s", bucket_name)

    except ClientError as e:
        code = e.response["Error"]["Code"]

        # More accurate, recruiter-friendly messaging
        if code == "BucketAlreadyOwnedByYou":
            logging.info("Bucket already exists and is owned by you: %s", bucket_name)
            return

        logging.error("CreateBucket failed (%s): %s", code, e)
        raise


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Import the boto3 library (handled above)
    # Instantiate a boto3 S3 client (client preferred over resource)
    session = boto3.session.Session()
    region = session.region_name or "us-east-1"

    # Name the bucket (must be globally unique in AWS)
    bucket_name = f"zonique-crud-{int(time.time())}"

    create_bucket(bucket_name=bucket_name, region=region)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())





