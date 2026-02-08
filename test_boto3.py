import boto3
print("boto3:", boto3.__version__)

sts = boto3.client("sts")
print(sts.get_caller_identity())

