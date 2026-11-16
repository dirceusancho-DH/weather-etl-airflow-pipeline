import pandas as pd
from pathlib import Path
import json


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent.parent / 'data' / 'weather_data.json'

columns_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "city_cod",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "sys_country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset"
}
columns_to_normalize = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.info(f"Creating DataFrame from file: {path_name}")
    path = Path(path_name)
    if not path.exists():
        raise FileNotFoundError(f"The file {path_name} does not exist.") 
     

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    print("ORIGINAL COLUMNS:", df.columns.tolist())
    logging.info(f"\n DataFrame created with length: {len(df)}\n")
    return df
   
def normalize_wether_comlumns(df: pd.DataFrame) -> pd.DataFrame:
    
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))
    df_weather = df_weather.rename(columns={
        'id': 'weather_id', 
        'main': 'weather_main', 
        'description': 'weather_description', 
        'icon': 'weather_icon'    
    })
    df = pd.concat([df.drop(columns=['weather']), df_weather], axis=1)
    logging.info(f"\n Normalized DataFrame columns: {df.columns.tolist()}\n")
    return df

def drop_columns(df: pd.DataFrame, columns_to_drop: list[str]) -> pd.DataFrame:

    logging.info(f"Dropping columns: {columns_to_drop}")   
    df = df.drop(columns=columns_to_drop, errors='ignore')
    logging.info(f"\n Dropped columns: {columns_to_drop}\n")
    return df

def rename_columns(df: pd.DataFrame, columns_names: dict[str, str]) -> pd.DataFrame:
    logging.info("Renaming columns")
    df = df.rename(columns=columns_names)
    logging.info(f"\n Renamed DataFrame columns: {df.columns.tolist()}\n")
    return df

def normalize_datetime_column(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    for name in columns_name:
        logging.info(f"Normalizing datetime column: {name}")
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('Europe/London')
        logging.info(f"\n Normalized datetime column: {name}\n")
    return df

def data_transformation():
    print("Starting data transformation process...")
    df = create_dataframe(path_name)
    df = normalize_wether_comlumns(df)
    df = drop_columns(df, columns_to_drop)
    df = rename_columns(df, columns_to_rename)
    df = normalize_datetime_column(df, columns_to_normalize)
    logging.info(f"\n Final DataFrame columns: {df.columns.tolist()}\n")
    return df
