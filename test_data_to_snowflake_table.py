# Import required libraries
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas
import os
from dotenv import load_dotenv
import pandas as pd
import random
from mimesis import Person
from mimesis.locales import Locale

load_dotenv()
# Connect to Snowflake using environment variables for sensitive information

conn = connect(
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    account=os.getenv('ACCOUNT'),
    warehouse=os.getenv('WAREHOUSE'),
    database=os.getenv('DATABASE'),
    schema=os.getenv('SCHEMA')
)

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


# Write the DataFrame to a Snowflake table
success, nchunks, nrows, _ = write_pandas(conn, emp_df, 'EMPLOYEES')
print(f"Status: {success}")
print(f"✅ Loaded {nrows} rows into Snowflake!")


# Close the connection to Snowflake
conn.close()