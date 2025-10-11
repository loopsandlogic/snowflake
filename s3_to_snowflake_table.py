from snowflake.connector import connect
import os
from dotenv import load_dotenv


load_dotenv()

# Get AWS credentials from environment variables

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION=os.getenv('AWS_DEFAULT_REGION')

# Set your bucket name and file details
bucket_name = 'pulastya-test-bucket'

# Connect to Snowflake using environment variables for sensitive information

conn = connect(
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    account=os.getenv('ACCOUNT'),
    warehouse=os.getenv('WAREHOUSE'),
    database=os.getenv('DATABASE'),
    schema=os.getenv('SCHEMA')
)

cs = conn.cursor()

# Check the current database and schema
cs.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
print(cs.fetchone())

# Create stage for S3 (using AWS keys)
cs.execute(f"""
        CREATE OR REPLACE STAGE my_s3_stage
        URL='s3://{bucket_name}/snowflake/'
        CREDENTIALS=(AWS_KEY_ID='{AWS_ACCESS_KEY_ID}' AWS_SECRET_KEY='{AWS_SECRET_ACCESS_KEY}')
        FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
        """)

# List stage to verify files
cs.execute("LIST @my_s3_stage")
print("Files in stage:")
for row in cs.fetchall():
    print(row)

# Copy data from S3 into table
cs.execute("""
        COPY INTO EMPLOYEES
        FROM @my_s3_stage/employee_df.csv
        FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
        """)


print("✅ Data loaded from S3 to Snowflake table EMPLOYEES.")

# Close connections
cs.close()
conn.close()