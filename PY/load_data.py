# Author: Shyamanth Lingampally

# Loads the UCI Steel Industry Energy Consumption dataset.
#
# Before running:
# 1. Download from https://archive.ics.uci.edu/dataset/851/steel+industry+energy+consumption
# 2. Save to your desktop (or update RAW_FILE path below)
#
# The raw file has 35,040 rows - one for each 15-min interval in 2018.
# This script cleans up column names, parses dates, adds a few useful columns,
# and saves a working copy for the rest of the pipeline.

import pandas as pd
import os
import sys


RAW_FILE = '/Users/shyamanthlingampally/Desktop/Steel_industry_data.csv'
CLEAN_FILE = '/Users/shyamanthlingampally/Desktop/energy_clean.csv'


# check that we have the raw file
if not os.path.exists(RAW_FILE):
    print(f'error: {RAW_FILE} not found')
    print('download the dataset first from UCI and save to the data folder')
    sys.exit(1)


# read the file
df = pd.read_csv(RAW_FILE)
print(f'loaded {len(df):,} rows')


# the raw column names have dots and parentheses which are annoying
# clean them up so they're easier to reference
new_columns = []
for col in df.columns:
    clean = col.strip().replace('.', '_').replace('(', '').replace(')', '')
    new_columns.append(clean)
df.columns = new_columns


# parse the date column - it's in DD/MM/YYYY HH:MM format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')


# pull out useful time components so we don't have to keep calculating them
df['hour'] = df['date'].dt.hour
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%b')
df['day_num'] = df['date'].dt.day


# load_type comes with underscores (Light_Load, Medium_Load, Maximum_Load)
# easier to read without them
df['Load_Type'] = df['Load_Type'].str.replace('_', ' ')


# save the cleaned version
df.to_csv(CLEAN_FILE, index=False)


# quick sanity check
print(f'date range: {df["date"].min()} to {df["date"].max()}')
print(f'avg usage per interval: {df["Usage_kWh"].mean():.1f} kWh')
print(f'load types: {df["Load_Type"].unique().tolist()}')
print(f'saved to {CLEAN_FILE}')
