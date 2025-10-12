# Import required libraries
from snowflake.connector import connect
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


query = """SELECT department
           , COUNT(id) AS employee_count
           ,avg(salary) AS avg_salary
           ,min(salary) AS min_salary
           ,max(salary) AS max_salary
           FROM employees
           GROUP BY department;"""

emp_df = pd.read_sql(query, conn)

# Close the connection to Snowflake
conn.close()


x = np.arange(len(emp_df['DEPARTMENT']))
width = 0.2

fig, ax1 = plt.subplots(figsize=(14, 7))

# --- Primary Y-axis (Employee Count) ---
ax1.bar(x - 1.5*width, emp_df['EMPLOYEE_COUNT'], width, label='Total Employees', color='black')
ax1.set_xlabel('Department')
ax1.set_ylabel('Employee Count', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# --- Secondary Y-axis (Salaries) ---
ax2 = ax1.twinx()
ax2.bar(x - 0.5*width, emp_df['AVG_SALARY'], width, label='Avg Salary', color='orange')
ax2.bar(x + 0.5*width, emp_df['MAX_SALARY'], width, label='Max Salary', color='green')
ax2.bar(x + 1.5*width, emp_df['MIN_SALARY'], width, label='Min Salary', color='red')
ax2.set_ylabel('Salary', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# --- Combine Legends ---
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')

plt.title('Department-wise Employee Count and Salary Summary')
plt.xticks(x, emp_df['DEPARTMENT'], rotation=45, ha='right')
plt.tight_layout()
plt.show()