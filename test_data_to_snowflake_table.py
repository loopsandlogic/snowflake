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

sc = conn.cursor()

person = Person(Locale.EN)

data = []
conunter = 100
for _ in range(100):
    conunter += 1
    emp = {
        "ID": conunter,
        "NAME": person.full_name(),
        "DEPARTMENT": random.choice(['HR', 'Engineering', 'Marketing', 'Sales']),
        "SALARY": random.randint(60000, 150000)
    }
    data.append(emp)

emp_df = pd.DataFrame(data, columns=['ID', 'NAME', 'DEPARTMENT', 'SALARY'])

# Truncate the table if it exists
sc.execute("TRUNCATE TABLE IF EXISTS EMPLOYEES")

# Write the DataFrame to a Snowflake table
success, nchunks, nrows, _ = write_pandas(conn, emp_df, 'EMPLOYEES')
print(f"Status: {success}")
print(f"✅ Loaded {nrows} rows into Snowflake!")


# Close the connection to Snowflake
conn.close()