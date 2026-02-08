import boto3

bucket_name = "zonique-boto3-test-264559555238"  # must be globally unique

s3 = boto3.client("s3", region_name="us-east-1")

s3.create_bucket(Bucket=bucket_name)

print("Bucket created:", bucket_name)
