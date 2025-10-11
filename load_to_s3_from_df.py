import boto3
import os
from dotenv import load_dotenv
import sys
import pandas as pd
from mimesis import Person
from mimesis.locales import Locale
from io import StringIO
import random

load_dotenv()

# Generate sample dataframe

person = Person(Locale.EN)

data = []
for _ in range(100):
    emp = {
        "ID": random.randint(100, 999),
        "NAME": person.full_name(),
        "DEPARTMENT": random.choice(['HR', 'Engineering', 'Marketing', 'Sales']),
        "SALARY": round(random.uniform(60000, 150000), 2)
    }
    data.append(emp)

emp_df = pd.DataFrame(data, columns=['ID', 'NAME', 'DEPARTMENT', 'SALARY'])

# Convert to CSV in memory
csv_buffer = StringIO()
emp_df.to_csv(csv_buffer, index=False)

# Get AWS credentials from environment variables

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION=os.getenv('AWS_DEFAULT_REGION')

# Set up S3 client

s3 = boto3.client('s3')

# Set your bucket name and file details
bucket_name = 'pulastya-test-bucket'
s3_file_key = 'snowflake/employee_df.csv'

s3.put_object(
    Bucket=bucket_name,
    Key=s3_file_key,
    Body=csv_buffer.getvalue()
)

print(f"✅ DataFrame uploaded to s3://{bucket_name}/{s3_file_key}")