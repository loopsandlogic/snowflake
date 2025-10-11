# load_to_dynamodb.py

import os
import boto3
from dotenv import load_dotenv
import pandas as pd
import sys
from mimesis import Person
import random

load_dotenv()

# AWS credentials and region from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)


# Initialize a dynamoDB session using the credentials and region
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)
table_name = 'Employees'
table = dynamodb.Table(table_name)

# Create the DynamoDB table if it doesn't exist
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'EmployeeID', 'KeyType': 'HASH'},  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'EmployeeID', 'AttributeType': 'N'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.wait_until_exists()
    print(f"Table {table_name} created successfully.")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    table = dynamodb.Table(table_name)
    print(f"Table {table_name} already exists.")

person = Person()

# Generate sample employee data using mimesis
data = []
for _ in range(100):
    emp = {
        "EmployeeID": random.randint(100, 999),
        "NAME": person.full_name(),
        "DEPARTMENT": random.choice(['HR', 'Engineering', 'Marketing', 'Sales']),
        "SALARY": random.randint(60000, 150000)
    }
    data.append(emp)

emp_df = pd.DataFrame(data)

# Insert data into the DynamoDB table
for index, row in emp_df.iterrows():
    table.put_item(Item=row.to_dict())
print("Data inserted successfully.")    

# Verify the data insertion
try:
    response = table.scan()
    items = response.get('Items', [])
    for item in items:
        print(item)
except Exception as e:
    print(f"Error scanning table: {e}")
    sys.exit(1)