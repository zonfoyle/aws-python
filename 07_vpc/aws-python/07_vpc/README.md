# VPC Public Network Setup (Boto3)

This script creates a basic public VPC setup using Python + Boto3:

- VPC (10.0.0.0/16)
- Internet Gateway attached to the VPC
- Public route table with `0.0.0.0/0 -> IGW`
- 3 public subnets across the first 3 available AZs
- Route table association for each subnet
- Tags applied to all resources

## Why this exists
This is a hands-on automation lab to practice AWS networking fundamentals and infrastructure automation using the AWS SDK.

## How to run
From the `aws-python` repo root:

```bash
cd 07_vpc
python3 vpc_public_network.py