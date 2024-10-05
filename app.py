import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# OpenWeatherMap API Key (replace with your own)
API_KEY = "3a5cc2310a48f3133b331faed7861fcd"


# Function to get current weather data
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("City not found!")
        return None

# Function to get weather forecast data for next few days
def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("City not found!")
        return None

# Streamlit app
st.title("Weather Dashboard")

# Input for city name
city = st.text_input("Enter City Name", "Pune")

if city:
    # Fetch weather data
    weather_data = get_weather_data(city)
    
    if weather_data:
        # Display current weather conditions
        st.subheader(f"Current Weather in {city}")
        st.write(f"**Temperature**: {weather_data['main']['temp']} °C")
        st.write(f"**Humidity**: {weather_data['main']['humidity']} %")
        st.write(f"**Wind Speed**: {weather_data['wind']['speed']} m/s")
        st.write(f"**Weather**: {weather_data['weather'][0]['description'].title()}")

        # Fetch weather forecast data
        forecast_data = get_forecast_data(city)
        
        if forecast_data:
            st.subheader(f"5-Day Forecast for {city}")

            # Extract date and temperature data
            forecast_dates = []
            forecast_temps = []
            for entry in forecast_data['list']:
                # Convert timestamp to datetime
                forecast_dates.append(datetime.utcfromtimestamp(entry['dt']))
                forecast_temps.append(entry['main']['temp'])

            # Plot the forecast data
            fig, ax = plt.subplots()
            ax.plot(forecast_dates, forecast_temps, marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title('5-Day Temperature Forecast')
            plt.xticks(rotation=45)

            st.pyplot(fig)

# To run this Streamlit app, type: `streamlit run app.py` in terminal.
