import boto3
import os
from dotenv import load_dotenv
import sys

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION=os.getenv('AWS_DEFAULT_REGION')


boto3.setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

s3 = boto3.client('s3')

bucket_name = 'pulastya-test-bucket'
local_file_path = '/Users/pulastya/Downloads/employee.csv'
s3_file_key = 'snowflake/employee.csv'

s3.upload_file(local_file_path, bucket_name, s3_file_key)
print(f"File {local_file_path} uploaded to s3://{bucket_name}/{s3_file_key}")