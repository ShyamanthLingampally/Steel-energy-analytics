# Author: Shyamanth Lingampally

# Loads the cleaned data into a SQLite database so we can run the queries
# in sql/queries.sql against it.

import sqlite3
import pandas as pd
import os


DB_PATH = '/Users/shyamanthlingampally/Desktop/energy.db'
CSV_PATH = '/Users/shyamanthlingampally/Desktop/energy_clean.csv'


# delete any existing db so we start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)


# load the csv and write to sqlite
df = pd.read_csv(CSV_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql('energy', conn, index=False)
conn.close()


print(f'database built at {DB_PATH}')
print(f'{len(df):,} rows loaded')
