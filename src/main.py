from src.tutorial_pipeline_dh.extract_data import extract_weather_data
from src.loadD import load_data
from src.tutorial_pipeline_dh.tranfosrm_data import data_transformation

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv('api_key')

url = f"http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid={API_KEY}"
table_name = 'lon_weather'

def pipeline():
    try:
        logging.info("Starting the ETL pipeline.")
        extract_weather_data(url)
        df_transformed = data_transformation()
        
        load_data(table_name, df_transformed)
        logging.info("ETL pipeline completed successfully.")

        print("\n" + "="*60)
        print("ETL Pipeline Completed.")
        print("="*60) 
    except Exception as e:
        logging.error(f"An error occurred during the ETL pipeline: {e}")
        import traceback
        traceback.print_exc()

pipeline() 

