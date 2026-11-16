from sqlalchemy import create_engine,text
from urllib.parse import quote_plus
import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)

user=os.getenv('user')
password=os.getenv('password')
database=os.getenv('database')

host='host.docker.internal'

def get_engine():
    logging.info(f"Creating database engine for user: {user}, database: {database}, host: {host}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
        )
engine = get_engine()

def load_data(table_name: str, df):
    logging.info(f"Loading data into table: {table_name}")
    
    df.to_sql(
             table_name,
             con=engine, 
             if_exists='append', 
             index=False
        )
    logging.info(f"Data loaded into table: {table_name} successfully.")
    df_check = pd.read_sql_query(f"SELECT * FROM {table_name}", con=engine)
    logging.info(f"Data check: {len(df_check)} records found in table: {table_name}.")
    