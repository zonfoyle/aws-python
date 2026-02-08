"""
Purpose:
    Create an S3 bucket safely using boto3.

Permissions required:
    s3:CreateBucket

Usage:
    python 02_s3/create_bucket.py --name my-unique-bucket-123
    python 02_s3/create_bucket.py --name my-unique-bucket-123 --region us-west-2
"""

from __future__ import annotations

import argparse
import logging
import sys

import boto3
from botocore.exceptions import ClientError


LOG = logging.getLogger(__name__)


def create_bucket(bucket_name: str, region: str) -> None:
    """
    Create an S3 bucket in the specified AWS region.
    """

    s3 = boto3.client("s3", region_name=region)

    try:
        # us-east-1 requires a different call format
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )

        LOG.info("Bucket created successfully: %s", bucket_name)

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "BucketAlreadyOwnedByYou":
            LOG.warning("Bucket already exists and is owned by you: %s", bucket_name)

        elif error_code == "BucketAlreadyExists":
            LOG.error("Bucket name taken globally. Choose another name.")

        else:
            LOG.error("Unexpected AWS error: %s", e)
            raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an AWS S3 bucket")
    parser.add_argument(
        "--name",
        required=True,
        help="Globally unique S3 bucket name",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    args = parse_args()
    create_bucket(args.name, args.region)

    return 0


if __name__ == "__main__":
    sys.exit(main())
