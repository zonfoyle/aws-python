"""
Purpose:
    List all S3 buckets in the AWS account.

Permissions required:
    s3:ListAllMyBuckets

Usage:
    python 01_setup/list_buckets.py
"""

from __future__ import annotations

import logging
import sys

import boto3
from botocore.exceptions import ClientError


LOG = logging.getLogger(__name__)


def list_buckets() -> None:
    """Retrieve and display all S3 buckets."""

    s3 = boto3.client("s3")

    try:
        response = s3.list_buckets()

        buckets = response.get("Buckets", [])

        if not buckets:
            LOG.info("No S3 buckets found.")
            return

        LOG.info("Found %s buckets:", len(buckets))

        for bucket in buckets:
            LOG.info(" - %s", bucket["Name"])

    except ClientError as e:
        LOG.error("AWS error occurred: %s", e)
        raise


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    list_buckets()
    return 0


if __name__ == "__main__":
    sys.exit(main())
