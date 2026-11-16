# 🌦️ London Weather ETL Pipeline

**An Automated Weather Data Pipeline Using Python, Apache Airflow, Docker, PostgreSQL, and Streamlit**

An end-to-end data engineering project that extracts London weather observations from the **OpenWeather API**, transforms the data using **Python and Pandas**, and loads the processed records into a **PostgreSQL database**.

The ETL workflow is orchestrated by **Apache Airflow**, running in a Docker environment. An interactive **Streamlit dashboard** uses Plotly to visualize the weather observations stored in PostgreSQL.

The project brings together API integration, data processing, relational database storage, workflow orchestration, and data visualization in a single system.

---

## 📌 Project Overview

The system collects current weather information for **London, United Kingdom**, through the OpenWeather API.

Each pipeline execution follows three main stages:

1. **Extract:** Retrieve weather data from the API.
2. **Transform:** Clean, flatten, and structure the API response.
3. **Load:** Insert the transformed observations into PostgreSQL.

Apache Airflow manages task execution and dependencies, while the Streamlit dashboard provides an interface for exploring the collected data.

The pipeline uses an append-based loading strategy, allowing observations to accumulate over time.

## 🏗️ System Architecture

```text
                  OpenWeather API
                         |
                         v
                  Python Extraction
                         |
                         v
                 Pandas Transformation
                         |
                         v
                  PostgreSQL Database
                    (lon_weather)
                         |
                         v
                  Streamlit Dashboard
                    + Plotly Charts
```

**Apache Airflow** orchestrates the extraction, transformation, and loading tasks.

**Docker** provides the environment in which the Airflow services run.

**PostgreSQL** stores the transformed weather observations.

**Streamlit and Plotly** provide interactive visualization and exploration of the stored data.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL development and application logic |
| OpenWeather API | Source of weather observations |
| Pandas | JSON processing and data transformation |
| PostgreSQL | Relational database storage |
| SQLAlchemy | Database connectivity |
| Apache Airflow | Workflow orchestration and scheduling |
| Docker | Containerized Airflow environment |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts and visualizations |
| uv | Python dependency management |
| Git & GitHub | Version control |
| VS Code | Development environment |

---

## 🔄 ETL Pipeline

### 1. Extract

The extraction process sends a request to the OpenWeather API to retrieve the latest available weather observation for London.

The response includes weather information such as:

- Temperature
- Feels-like temperature
- Minimum and maximum temperature
- Humidity
- Atmospheric pressure
- Wind speed
- Geographic coordinates
- Weather observation timestamp

The API request uses metric units, so temperatures are returned in **degrees Celsius**.

### 2. Transform

The transformation stage uses Python and Pandas to convert the API response into a structured DataFrame.

The transformation process includes:

- Flattening nested JSON data
- Renaming columns using `snake_case`
- Converting Unix timestamps into datetime values
- Processing weather measurements
- Preparing a consistent structure for database insertion

Examples of transformed columns:

```text
datetime
city_name
temperature
feels_like
temp_min
temp_max
humidity
pressure
wind_speed
longitude
latitude
```

### 3. Load

The transformed data is loaded into PostgreSQL using SQLAlchemy.

**Database:** `tutorial_weather_data`  
**Table:** `lon_weather`

The load process uses:

```python
if_exists="append"
```

This preserves existing records and inserts new observations during subsequent pipeline executions.

The pipeline does not currently enforce uniqueness on observation timestamps. As a result, repeated API readings can be stored when the pipeline runs multiple times before OpenWeather publishes a new observation.

---

## ⏰ Apache Airflow Orchestration

Apache Airflow is used to automate and monitor the ETL workflow.

The DAG is defined in:

```text
dags/weather_dag.py
```

The workflow follows the task dependency sequence:

```text
Extract
   |
   v
Transform
   |
   v
Load
```

### Airflow Capabilities

- Automated workflow scheduling
- Manual DAG triggering
- Task dependency management
- Execution monitoring
- Task-level logging
- Failed-task identification
- Workflow run history

The Airflow services run inside Docker containers.

The PostgreSQL database used to store the weather observations runs locally and is accessed by the pipeline.

---

## 🗄️ PostgreSQL Database

PostgreSQL serves as the primary data storage layer.

The `lon_weather` table contains the transformed weather observations collected during pipeline executions.

Example SQL query:

```sql
SELECT
    datetime,
    city_name,
    temperature,
    feels_like,
    humidity,
    wind_speed,
    pressure
FROM lon_weather
ORDER BY datetime DESC;
```

To check the total number of stored records:

```sql
SELECT COUNT(*)
FROM lon_weather;
```

### Data Storage Approach

The pipeline uses append-based loading.

Each successful load inserts the retrieved observation without replacing the existing dataset.

This allows the database to retain measurements collected across multiple executions.

**Important:** Because the source is a current-weather API, repeated pipeline executions can return identical measurements or timestamps. The project currently preserves these records rather than automatically removing duplicates.

---

## 📊 London Weather Dashboard

The project includes an interactive dashboard built with **Streamlit** and **Plotly**.

The dashboard connects directly to PostgreSQL and visualizes the weather observations stored in the `lon_weather` table.

### Dashboard Features

**Weather Observation Cards**

- Five compact cards displaying the most recent observations
- Light-blue highlighting for the latest reading
- Temperature displayed in degrees Celsius
- Observation date and time
- Humidity and wind speed measurements

The cards show the five most recent records, but the database can contain many more observations.

**Weather Metrics**

The dashboard displays measurements from the latest stored observation:

- Temperature
- Feels-like temperature
- Humidity
- Wind speed
- Atmospheric pressure

**Interactive Weather Charts**

Plotly is used to visualize:

- Temperature history
- Temperature versus feels-like temperature
- Humidity changes
- Wind speed measurements
- Atmospheric pressure measurements

**Additional Functionality**

- Interactive London location map
- Observation history filters
- Manual data refresh
- Expandable observation table
- CSV download functionality
- Dark-themed interface

### Observation Data

The dashboard displays **collected weather observations**, not future weather forecasts.

The five weather cards represent recent database records rather than five forecast days.

Charts and the observation explorer provide access to the wider collection of stored measurements.

As the pipeline collects more observations, the historical visualizations become more informative.

---

## 📁 Project Structure

The main project files and directories include:

```text
weather-etl-airflow-pipeline/
│
├── dags/
│   └── weather_dag.py
│
├── src/
│   ├── main.py
│   ├── loadD.py
│   └── tutorial_pipeline_dh/
│       └── tranfosrm_data.py
│
├── config/
│   └── .env                  # Local credentials; not committed
│
├── dashboard.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

Docker configuration files and additional supporting project files are maintained alongside the application code.

---

## 🚀 Installation and Setup

### Prerequisites

The following tools are required:

- Python
- uv
- PostgreSQL
- Docker Desktop
- Git
- OpenWeather API key

### 1. Clone the Repository

```bash
git clone https://github.com/dirceusancho-DH/weather-etl-airflow-pipeline.git
cd weather-etl-airflow-pipeline
```

### 2. Install Dependencies

The project uses `uv` for Python environment and dependency management.

```bash
uv sync
```

### 3. Configure Database Credentials

Create a `config/.env` file with your PostgreSQL connection settings.

Example:

```dotenv
user=YOUR_POSTGRES_USER
password=YOUR_POSTGRES_PASSWORD
database=tutorial_weather_data
```

The Streamlit dashboard currently connects to PostgreSQL using:

```text
localhost:5432
```

The OpenWeather API key must also be configured according to the extraction module's environment-variable requirements.

Docker-related environment variables should be configured in the project's root `.env` file as required by the Docker Compose setup.

**Security:** Actual API keys, passwords, and `.env` files must not be committed to the repository.

### 4. Prepare PostgreSQL

Start the PostgreSQL service and create the database if it does not already exist.

```sql
CREATE DATABASE tutorial_weather_data;
```

Ensure the configured database user has permission to connect to the database and create or insert records into the required table.

### 5. Start Apache Airflow

From the project directory, start the Docker services:

```bash
docker compose up -d
```

Open the Airflow web interface using the port configured in the Docker Compose setup.

Enable the weather DAG and trigger a run.

Monitor the tasks until the extraction, transformation, and loading stages have completed successfully.

### 6. Verify Stored Observations

Connect to PostgreSQL and run:

```sql
SELECT *
FROM lon_weather
ORDER BY datetime DESC;
```

The query should return weather observations inserted by successful pipeline executions.

### 7. Run the Streamlit Dashboard

Start the dashboard:

```bash
uv run streamlit run dashboard.py
```

Open the application in your browser:

```text
http://localhost:8501
```

The dashboard reads from PostgreSQL and displays the available London weather observations.

---

## 🔍 Data Quality and Limitations

The current implementation has several important characteristics.

### Repeated Observations

The OpenWeather current-weather endpoint can return the same observation across multiple requests.

Because the pipeline appends each retrieved record, duplicate timestamps and measurements can occur.

### Historical Data Collection

The pipeline builds its historical dataset from observations collected during its executions.

It does not automatically retrieve a complete historical weather archive.

### Local Database Dependency

The Streamlit dashboard requires access to the PostgreSQL database.

If the local PostgreSQL server is unavailable, the dashboard cannot retrieve its data.

### Forecast Availability

The project currently uses current-weather observations.

Forecast information is not included in the dashboard.

---

## ☁️ Deployment Status

**Current status: Local development**

The ETL pipeline, Airflow environment, PostgreSQL database, and Streamlit dashboard are currently configured for local execution.

The dashboard is accessible locally at:

```text
http://localhost:8501
```

### Public Deployment

Public deployment is a possible future extension.

Because the dashboard currently uses a local PostgreSQL connection, deploying Streamlit to a remote hosting service would require a cloud-accessible database or another hosted data source.

The existing `localhost:5432` connection cannot directly access the developer's local database from a remote Streamlit server.

---

## 🔮 Future Improvements

Potential enhancements include:

- Deploying the Streamlit dashboard online
- Migrating PostgreSQL to a hosted database
- Adding duplicate detection or upsert logic
- Implementing automated data quality checks
- Adding pipeline execution notifications
- Expanding weather history analysis
- Introducing forecast data through a suitable API endpoint
- Adding automated tests for extraction and transformation logic

---

## 📌 Project Status

| Component | Status |
|---|---|
| OpenWeather API extraction | Implemented |
| Pandas data transformation | Implemented |
| PostgreSQL data loading | Implemented |
| Apache Airflow orchestration | Running locally |
| Docker environment | Running locally |
| Streamlit dashboard | Implemented locally |
| Interactive Plotly visualizations | Implemented |
| Public dashboard deployment | Not yet implemented |

---

##  Author

**dirceusancho-DH**
**Buededados**

GitHub: https://github.com/dirceusancho-DH

---

*London Weather ETL Pipeline — automated weather data extraction, transformation, storage, orchestration, and visualization.*