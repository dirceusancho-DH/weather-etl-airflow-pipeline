
import os
from pathlib import Path
from urllib.parse import quote_plus
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="London Weather Studio",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

load_dotenv(Path(__file__).parent / "config" / ".env")

DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_NAME = os.getenv("database")


@st.cache_resource
def get_engine():
    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError(
            "Database credentials missing from config/.env"
        )

    return create_engine(
        "postgresql+psycopg2://"
        f"{quote_plus(DB_USER)}:"
        f"{quote_plus(DB_PASSWORD)}"
        f"@localhost:5432/{quote_plus(DB_NAME)}",
        pool_pre_ping=True,
    )


@st.cache_data(ttl=60)
def get_weather():
    with get_engine().connect() as connection:
        return pd.read_sql_query(
            text(
                "SELECT * FROM lon_weather ORDER BY datetime DESC"
            ),
            connection,
        )


# ============================================================
# HELPERS
# ============================================================

def fmt(value, decimals=1):
    if pd.isna(value):
        return "—"
    return f"{float(value):.{decimals}f}"


def safe(value):
    return escape(str(value))


def chart_style(fig, height=320):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="#191c23",
        plot_bgcolor="#191c23",
        font=dict(
            family="Arial",
            color="#d6dce5",
            size=12,
        ),
        margin=dict(l=15, r=15, t=30, b=15),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            y=1.14,
            x=0,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
        ),
    )
    return fig


def section(title, subtitle=""):
    st.markdown(
        f"""
<div class="section-title">{safe(title)}</div>
<div class="section-subtitle">{safe(subtitle)}</div>
""".strip(),
        unsafe_allow_html=True,
    )


def metric_card(label, value, note):
    html = (
        '<div class="metric-card">'
        f'<div class="metric-label">{safe(label)}</div>'
        f'<div class="metric-value">{safe(value)}</div>'
        f'<div class="metric-note">{safe(note)}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #101217;
    color: #f4f6fa;
}

.block-container {
    max-width: 1480px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 28px;
}

.brand {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f4f6fa;
}

.brand span {
    color: #bce8ff;
}

.location-pill {
    font-size: 12px;
    color: #aeb7c5;
    background: #1c2028;
    border: 1px solid #2c313b;
    padding: 10px 15px;
    border-radius: 30px;
}

.eyebrow {
    font-size: 11px;
    letter-spacing: 2px;
    color: #a3b0c0;
    font-weight: 700;
    margin-bottom: 9px;
}

.hero-title {
    font-size: clamp(31px, 4vw, 48px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -1.8px;
    color: #f4f6fa;
}

.hero-subtitle {
    font-size: 13px;
    color: #929eae;
    margin-top: 10px;
    margin-bottom: 22px;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #f4f6fa;
    margin-top: 25px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #8e9aaa;
    font-size: 12px;
    margin-bottom: 16px;
}

.weather-card {
    border-radius: 18px;
    background: #1f232c;
    border: 1px solid #2a303a;
    padding: 16px 12px;
    min-height: 174px;
    transition: transform 0.2s ease;
}

.weather-card:hover {
    transform: translateY(-3px);
}

.weather-card.selected {
    background: #c7e9fa;
    border-color: #c7e9fa;
}

.card-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #a5b2c2;
}

.selected .card-label {
    color: #456175;
}

.card-icon {
    font-size: 24px;
    margin: 8px 0 5px;
}

.card-temp {
    font-size: clamp(22px, 2.4vw, 32px);
    font-weight: 800;
    letter-spacing: -1px;
    color: #f5f7fa;
}

.selected .card-temp {
    color: #172333;
}

.card-date {
    font-size: 10px;
    color: #9daaba;
    margin: 6px 0 10px;
}

.selected .card-date {
    color: #4b6679;
}

.card-details {
    font-size: 10px;
    color: #b5bfcb;
    line-height: 1.8;
}

.selected .card-details {
    color: #344f61;
}

.metric-card {
    background: #1c2028;
    border: 1px solid #292f38;
    border-radius: 17px;
    padding: 18px 15px;
    min-height: 120px;
}

.metric-label {
    font-size: 11px;
    color: #a5afbf;
    margin-bottom: 11px;
}

.metric-value {
    font-size: clamp(19px, 2vw, 28px);
    font-weight: 800;
    letter-spacing: -0.7px;
    color: #f5f7fa;
}

.metric-note {
    font-size: 10px;
    color: #8290a2;
    margin-top: 7px;
}

.chart-label {
    font-size: 16px;
    font-weight: 800;
    color: #f4f6fa;
    margin-top: 12px;
}

.chart-subtitle {
    font-size: 11px;
    color: #8d99a9;
    margin-top: 4px;
    margin-bottom: 6px;
}

.insight-card {
    background: #1c2028;
    border: 1px solid #2a303a;
    border-radius: 16px;
    padding: 17px;
    margin-bottom: 11px;
}

.insight-label {
    font-size: 11px;
    color: #a3afbe;
    margin-bottom: 8px;
}

.insight-value {
    font-size: 22px;
    font-weight: 800;
    color: #f4f6fa;
}

.footer-note {
    font-size: 11px;
    color: #798595;
    text-align: center;
    margin-top: 35px;
    line-height: 1.8;
}

div[data-testid="stPlotlyChart"] {
    background: #191c23;
    border: 1px solid #272c35;
    border-radius: 18px;
    padding: 5px;
}

@media (max-width: 800px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .topbar {
        flex-direction: column;
        align-items: flex-start;
    }

    .weather-card {
        padding: 12px 8px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

try:
    df = get_weather()

except Exception as exc:
    st.error("Could not connect to PostgreSQL.")
    st.code(str(exc))
    st.stop()


if df.empty:
    st.warning(
        "No weather data found. Trigger the Airflow DAG first."
    )
    st.stop()


df["datetime"] = pd.to_datetime(
    df["datetime"],
    utc=True,
    errors="coerce",
)

df = df.dropna(subset=["datetime"])

numeric_columns = [
    "temperature",
    "feels_like",
    "humidity",
    "wind_speed",
    "pressure",
    "temp_min",
    "temp_max",
    "longitude",
    "latitude",
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


required = [
    "temperature",
    "feels_like",
    "humidity",
    "wind_speed",
    "pressure",
]

missing = [
    col for col in required
    if col not in df.columns
]

if missing:
    st.error(
        "Missing PostgreSQL columns: "
        + ", ".join(missing)
    )
    st.stop()


df = df.sort_values("datetime").reset_index(drop=True)

if df.empty:
    st.warning("No valid observation timestamps found.")
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="topbar">
    <div class="brand">weather<span>studio.</span></div>
    <div class="location-pill">📍 London, United Kingdom</div>
</div>
<div class="eyebrow">YOUR CITY, YOUR WEATHER</div>
<div class="hero-title">
    London's weather,<br>
    beautifully simple.
</div>
<div class="hero-subtitle">
    Real London weather observations, all in one place.
</div>
""".strip(),
    unsafe_allow_html=True,
)


# ============================================================
# FILTER AND REFRESH
# ============================================================

filter_col, refresh_col = st.columns(
    [3, 1],
    vertical_alignment="bottom",
)

with filter_col:
    period = st.selectbox(
        "Observation history",
        [
            "All observations",
            "Last 24 hours",
            "Last 7 days",
            "Last 30 days",
        ],
    )

with refresh_col:
    if st.button(
        "↻ Refresh weather",
        use_container_width=True,
    ):
        get_weather.clear()
        st.rerun()


filtered = df.copy()

if period != "All observations":
    hours = {
        "Last 24 hours": 24,
        "Last 7 days": 168,
        "Last 30 days": 720,
    }[period]

    cutoff = (
        pd.Timestamp.now(tz="UTC")
        - pd.Timedelta(hours=hours)
    )

    filtered = filtered[
        filtered["datetime"] >= cutoff
    ].copy()


if filtered.empty:
    st.info(
        "No observations in this period. "
        "Select 'All observations'."
    )
    st.stop()


latest = filtered.iloc[-1]

latest_time = latest["datetime"].tz_convert(
    "Europe/London"
)


# ============================================================
# FIVE COMPACT LONDON WEATHER CARDS
# ============================================================

section(
    "🌤️ London weather",
    "The five latest recorded observations",
)

recent = filtered.tail(5).iloc[::-1]
card_columns = st.columns(5, gap="small")

for index, (_, observation) in enumerate(
    recent.iterrows()
):
    selected = index == 0

    observed_at = observation["datetime"].tz_convert(
        "Europe/London"
    )

    date_label = observed_at.strftime("%d %b · %H:%M")

    temp = fmt(observation["temperature"])
    humidity = fmt(observation["humidity"], 0)
    wind = fmt(observation["wind_speed"])

    card_class = (
        "weather-card selected"
        if selected
        else "weather-card"
    )

    label = (
        "LATEST"
        if selected
        else f"READING {index + 1}"
    )

    # IMPORTANT:
    # HTML starts at the beginning of the string.
    # No indentation means Streamlit will render
    # the card instead of displaying HTML tags.
    card_html = (
        f'<div class="{card_class}">'
        f'<div class="card-label">{label}</div>'
        '<div class="card-icon">🌡️</div>'
        f'<div class="card-temp">{safe(temp)}°C</div>'
        f'<div class="card-date">{safe(date_label)} UK</div>'
        '<div class="card-details">'
        f'💧 {safe(humidity)}% humidity<br>'
        f'💨 {safe(wind)} m/s wind'
        '</div>'
        '</div>'
    )

    with card_columns[index]:
        st.markdown(
            card_html,
            unsafe_allow_html=True,
        )


if len(recent) < 5:
    st.caption(
        f"{len(recent)} observation(s) available. "
        "More Airflow runs will add observations."
    )


# ============================================================
# WEATHER METRICS
# ============================================================

section(
    "Weather at a glance",
    "Measurements from the latest observation",
)

metrics = [
    (
        "🌡️ Temperature",
        f"{fmt(latest['temperature'])}°C",
        "Air temperature",
    ),
    (
        "🧥 Feels like",
        f"{fmt(latest['feels_like'])}°C",
        "Perceived temperature",
    ),
    (
        "💧 Humidity",
        f"{fmt(latest['humidity'], 0)}%",
        "Relative humidity",
    ),
    (
        "💨 Wind speed",
        f"{fmt(latest['wind_speed'])} m/s",
        "Wind measurement",
    ),
    (
        "🌬️ Pressure",
        f"{fmt(latest['pressure'], 0)} hPa",
        "Atmospheric pressure",
    ),
]

metric_columns = st.columns(5, gap="small")

for column, (label, value, note) in zip(
    metric_columns,
    metrics,
):
    with column:
        metric_card(label, value, note)


# ============================================================
# TEMPERATURE AND HUMIDITY
# ============================================================

section(
    "Weather trends",
    "Interactive charts from your real weather data",
)

temp_col, humidity_col = st.columns(
    [1.6, 1],
    gap="medium",
)

with temp_col:
    st.markdown(
        '<div class="chart-label">Temperature history</div>'
        '<div class="chart-subtitle">'
        'Temperature vs. feels-like temperature'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_temp = go.Figure()

    fig_temp.add_trace(
        go.Scatter(
            x=filtered["datetime"],
            y=filtered["temperature"],
            name="Temperature",
            mode="lines+markers",
            line=dict(
                color="#bfeaff",
                width=3,
            ),
            marker=dict(size=7),
        )
    )

    fig_temp.add_trace(
        go.Scatter(
            x=filtered["datetime"],
            y=filtered["feels_like"],
            name="Feels like",
            mode="lines+markers",
            line=dict(
                color="#a995ff",
                width=2,
                dash="dot",
            ),
            marker=dict(size=6),
        )
    )

    chart_style(fig_temp, 330)
    fig_temp.update_yaxes(title_text="°C")

    st.plotly_chart(
        fig_temp,
        use_container_width=True,
        theme=None,
    )


with humidity_col:
    st.markdown(
        '<div class="chart-label">Humidity levels</div>'
        '<div class="chart-subtitle">'
        'Relative humidity over time'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_humidity = go.Figure()

    fig_humidity.add_trace(
        go.Bar(
            x=filtered["datetime"],
            y=filtered["humidity"],
            name="Humidity",
            marker_color="#91c8e8",
        )
    )

    chart_style(fig_humidity, 330)

    fig_humidity.update_yaxes(
        title_text="Humidity (%)",
        range=[0, 100],
    )

    st.plotly_chart(
        fig_humidity,
        use_container_width=True,
        theme=None,
    )


# ============================================================
# WIND AND PRESSURE
# ============================================================

wind_col, pressure_col = st.columns(
    2,
    gap="medium",
)

with wind_col:
    st.markdown(
        '<div class="chart-label">Wind speed</div>'
        '<div class="chart-subtitle">'
        'Measured in metres per second'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_wind = go.Figure()

    fig_wind.add_trace(
        go.Scatter(
            x=filtered["datetime"],
            y=filtered["wind_speed"],
            mode="lines+markers",
            name="Wind speed",
            line=dict(
                color="#91e2cb",
                width=3,
            ),
            marker=dict(size=7),
        )
    )

    chart_style(fig_wind, 300)
    fig_wind.update_yaxes(title_text="m/s")

    st.plotly_chart(
        fig_wind,
        use_container_width=True,
        theme=None,
    )


with pressure_col:
    st.markdown(
        '<div class="chart-label">Atmospheric pressure</div>'
        '<div class="chart-subtitle">'
        'Measured in hectopascals'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_pressure = go.Figure()

    fig_pressure.add_trace(
        go.Scatter(
            x=filtered["datetime"],
            y=filtered["pressure"],
            mode="lines+markers",
            name="Pressure",
            line=dict(
                color="#ffc991",
                width=3,
            ),
            marker=dict(size=7),
        )
    )

    chart_style(fig_pressure, 300)
    fig_pressure.update_yaxes(title_text="hPa")

    st.plotly_chart(
        fig_pressure,
        use_container_width=True,
        theme=None,
    )


# ============================================================
# MAP AND INSIGHTS
# ============================================================

section(
    "Explore London",
    "Location and latest weather details",
)

map_col, insight_col = st.columns(
    [1.7, 1],
    gap="medium",
)

with map_col:
    st.markdown(
        '<div class="chart-label">London on the map</div>'
        '<div class="chart-subtitle">'
        'Weather observation location'
        '</div>',
        unsafe_allow_html=True,
    )

    longitude = (
        latest["longitude"]
        if "longitude" in latest.index
        and pd.notna(latest["longitude"])
        else -0.1276
    )

    latitude = (
        latest["latitude"]
        if "latitude" in latest.index
        and pd.notna(latest["latitude"])
        else 51.5072
    )

    fig_map = go.Figure()

    fig_map.add_trace(
        go.Scattergeo(
            lon=[longitude],
            lat=[latitude],
            text=["London"],
            mode="markers+text",
            textposition="top center",
            marker=dict(
                size=15,
                color="#bfeaff",
                line=dict(
                    width=2,
                    color="#ffffff",
                ),
            ),
            textfont=dict(
                color="#f5f7fa",
                size=13,
            ),
            hovertemplate=(
                "London, United Kingdom"
                "<extra></extra>"
            ),
        )
    )

    fig_map.update_geos(
        scope="europe",
        projection_type="natural earth",
        showland=True,
        landcolor="#2b303a",
        showocean=True,
        oceancolor="#151a23",
        showcountries=True,
        countrycolor="#48515d",
        bgcolor="#191c23",
        lataxis_range=[40, 62],
        lonaxis_range=[-15, 20],
    )

    fig_map.update_layout(
        height=355,
        paper_bgcolor="#191c23",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        theme=None,
    )


with insight_col:
    st.markdown(
        '<div class="chart-label">Latest details</div>'
        '<div class="chart-subtitle">'
        'From the most recent observation'
        '</div>',
        unsafe_allow_html=True,
    )

    min_temp = (
        fmt(latest["temp_min"])
        if "temp_min" in latest.index
        else "—"
    )

    max_temp = (
        fmt(latest["temp_max"])
        if "temp_max" in latest.index
        else "—"
    )

    insights = [
        ("🌡️ Minimum temperature", f"{min_temp}°C"),
        ("☀️ Maximum temperature", f"{max_temp}°C"),
        (
            "🕒 Last observation",
            latest_time.strftime("%d %b %Y · %H:%M"),
        ),
    ]

    for label, value in insights:
        st.markdown(
            (
                '<div class="insight-card">'
                f'<div class="insight-label">{safe(label)}</div>'
                f'<div class="insight-value">{safe(value)}</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


# ============================================================
# OBSERVATION TABLE
# ============================================================

section(
    "Observation explorer",
    "Explore the actual PostgreSQL records",
)

with st.expander(
    "📋 View weather observations",
    expanded=False,
):
    wanted_columns = [
        "datetime",
        "city_name",
        "temperature",
        "feels_like",
        "humidity",
        "wind_speed",
        "pressure",
        "temp_min",
        "temp_max",
    ]

    available_columns = [
        col for col in wanted_columns
        if col in filtered.columns
    ]

    table_df = filtered[
        available_columns
    ].sort_values(
        "datetime",
        ascending=False,
    )

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇ Download CSV",
        data=table_df.to_csv(index=False).encode("utf-8"),
        file_name="london_weather.csv",
        mime="text/csv",
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    (
        '<div class="footer-note">'
        'London Weather Studio'
        f' &nbsp; • &nbsp; {len(filtered)} observations'
        ' &nbsp; • &nbsp; '
        f'Latest: {safe(latest_time.strftime("%d %b %Y %H:%M"))}'
        ' UK time'
        '<br>'
        'Powered by real OpenWeather observations'
        '</div>'
    ),
    unsafe_allow_html=True,
)
