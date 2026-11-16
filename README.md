# Weather ETL Pipeline with Apache Airflow 🌦️

A data engineering project that extracts real-time weather data for London from the OpenWeather API, transforms it using Python and Pandas, and loads it into a PostgreSQL database.

The ETL workflow is orchestrated using Apache Airflow running in Docker.

## Technologies Used

- Python
- Apache Airflow 3.1.7
- Docker and Docker Compose
- PostgreSQL
- Pandas
- SQLAlchemy
- OpenWeather API
- uv (Python package management)

## ETL Pipeline

**OpenWeather API → Extract → Transform → Load → PostgreSQL**

1. **Extract:** Retrieve weather data for London from the OpenWeather API.
2. **Transform:** Process the extracted data using Python and Pandas.
3. **Load:** Store the transformed data in a PostgreSQL table named `lon_weather`.

Apache Airflow orchestrates the workflow through three tasks:

`extract → transform → load`

## Project Structure

```text
tutorial_pipeline_DH/
├── dags/
│   └── weather_dag.py
├── src/
│   ├── main.py
│   ├── loadD.py
│   └── tutorial_pipeline_dh/
├── notebooks/
│   └── analysis_data.ipynb
├── config/
├── data/
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

## Configuration

The project uses environment variables for API credentials and database connection settings.

Sensitive `.env` files are excluded from version control.

The Docker Compose configuration is intended for local development and requires environment-specific configuration.

## Current Status

- Weather data extraction working
- Data transformation working
- PostgreSQL loading working
- Apache Airflow DAG successfully executed
- SQL queries verified in pgAdmin 4

## Future Improvements

- Add data validation
- Prevent duplicate weather records
- Improve error handling
- Add automated tests
- Build a dashboard to visualize weather trends
