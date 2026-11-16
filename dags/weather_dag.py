from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys,os 
sys.path.insert(0, '/opt/airflow')


from src.tutorial_pipeline_dh.extract_data import extract_weather_data
from src.loadD import load_data
from src.tutorial_pipeline_dh.tranfosrm_data import data_transformation
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv('API_KEY')
url = f"http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&appid={API_KEY}"

@dag(
    dag_id='tutorial_weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='A simple ETL pipeline for weather data',
    schedule='0 * * * *',
    start_date=datetime(2026, 11, 16),
    catchup=False,
    tags=['weather', 'ETL', 'tutorial'],
)

def weather_etl_pipeline():
    @task()
    def extract():
        extract_weather_data(url)

    @task()
    def transform():    
        df=data_transformation()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task()
    def load():
        import pandas as pd
        df=pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_data('lon_weather', df)

    extract() >> transform() >> load()    

weather_dag = weather_etl_pipeline()  
