# Cloud Resource Manager

Cloud Resource Manager is a Python-based command-line project for automating the provisioning and management of AWS infrastructure.

This project was built to practice managing cloud resources programmatically instead of relying only on the AWS Management Console. It uses boto3 to create and manage core AWS services such as VPC components, EC2 instances, and IAM roles, with room to expand into additional services like S3 and monitoring workflows.

## Project Purpose

The goal of this project is to strengthen hands-on cloud engineering skills by automating common infrastructure tasks in AWS. Rather than creating every resource manually in the console, this project uses Python scripts and AWS SDK calls to provision infrastructure in a more repeatable and structured way. It is designed as a learning project, while also reflecting the kind of automation mindset used in cloud and DevOps environments.

## What the Project Does

This project currently includes scripts to:
- create a VPC
- create a subnet
- create an internet gateway
- create a route table
- launch an EC2 instance
- list EC2 instances
- filter EC2 instances
- stop EC2 instances by tag
- create an IAM role

The long-term goal is to combine these scripts into a more complete infrastructure automation workflow driven by configuration.

## Architecture

config.yaml
    ↓
Python CLI / scripts
    ↓
boto3
    ↓
AWS Infrastructure

## Technologies Used

- Python
- boto3
- PyYAML
- AWS EC2
- AWS IAM
- AWS VPC

## Project Structure

cloud-resource-manager/
├── README.md
├── requirements.txt
├── config.yaml
├── 01_create_vpc.py
├── 02_create_subnet.py
├── 03_create_internet_gateway.py
├── 04_create_route_table.py
├── 05_launch_ec2.py
├── 06_list_ec2_instances.py
├── 07_filter_ec2_instances.py
├── 08_stop_ec2_by_tag.py
└── 09_create_iam_role.py

## How to Run

1. Configure your AWS credentials
2. Install dependencies
3. Run the desired Python script

Example:

```bash
pip install -r requirements.txt
python 01_create_vpc.py