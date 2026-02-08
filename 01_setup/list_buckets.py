import boto3

s3 = boto3.client("s3")
resp = s3.list_buckets()

for b in resp["Buckets"]:
    print(b["Name"])
