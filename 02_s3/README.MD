# AWS Python Automation

Python automation projects using AWS SDK (Boto3).

This repository documents my hands-on learning and implementation of AWS automation workflows using Python, Terraform, and cloud engineering best practices.

---

## Project Goals

- Build real-world AWS automation scripts
- Practice infrastructure + SDK workflows
- Develop production-style Python structure
- Prepare for Solutions Architect / Cloud Engineering roles

---

## Tech Stack

- Python 3
- AWS SDK (Boto3)
- AWS CLI
- Virtual environments
- Git & GitHub

---

## Project Structure

aws-python/
│
├── 01_setup/
│   ├── test_boto3.py
│   ├── test_sts.py
│   └── list_buckets.py
│
├── 02_s3/
│   ├── create_bucket.py
│   ├── s3_crud.py
│   └── whoami.py
│
├── requirements.txt
└── README.md

---

## Example Project: S3 Automation

### s3_crud.py

Creates an S3 bucket using:

- region-aware deployment
- globally unique naming
- logging
- exception handling

Concepts demonstrated:

- AWS authentication via default credential chain
- SDK client usage
- bucket provisioning automation
- error handling with botocore

---

## How to Run

## 1) Clone the repo

git clone https://github.com/zonfoyle/aws-python.git
cd aws-python 

### 2) Create virtual environment

python -m venv .venv
source .venv/bin/activate

### 3) Install dependencies

pip install -r requirements.txt

### 4) Configure AWS credentials

aws configure

OR set environment variables:

export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
export AWS_DEFAULT_REGION=us-east-1

### 5) Run script

cd 02_s3
python s3_crud.py

---

## Security Notes

This repository:

- does NOT store AWS credentials
- uses environment-based authentication
- excludes `.venv/` and `.aws/` from version control
- avoids hardcoded account IDs

---

## Learning Focus

This repo is part of my cloud engineering journey:

- AWS Solutions Architect preparation
- Python automation for infrastructure
- Terraform + IaC (coming next)
- Production coding practices

---

## Upcoming Work

- Full S3 CRUD automation
- IAM automation scripts
- EC2 provisioning
- Terraform infrastructure modules
- Lambda automation

---

## Author

Zonique Foyle  
Cloud Engineering | AWS | Python Automation
