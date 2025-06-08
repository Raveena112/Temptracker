import streamlit as st
import requests
import os
from dotenv import load_dotenv
import datetime

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    
    # Debug info:
    print(response.url)  # shows full API URL
    print(response.status_code)
    print(response.text)  # shows the API error message
    
    return response.json()


def main():
    st.set_page_config(page_title="Weather Forecast App", page_icon="⛅")
    st.title("🌦️ Weather Forecast App")

    city = st.text_input("Enter city name", value="Hyderabad")

    if st.button("Get Forecast"):
        data = get_weather(city)
        if data.get("cod") == "200":
            st.success(f"Weather forecast for {data['city']['name']}, {data['city']['country']}")
            st.write("📅 5 Upcoming Forecasts:")

            for forecast in data["list"][:5]:  # 5 entries = next 15 hours (3hr intervals)
                time = datetime.datetime.fromtimestamp(forecast["dt"])
                temp = forecast["main"]["temp"]
                desc = forecast["weather"][0]["description"]
                humidity = forecast["main"]["humidity"]
                icon = forecast["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                
                st.write(f"### {time.strftime('%Y-%m-%d %H:%M')}")
                st.image(icon_url, width=80)
                st.write(f"🌡 Temperature: **{temp}°C**")
                st.write(f"💧 Humidity: **{humidity}%**")
                st.write(f"☁️ Description: **{desc.capitalize()}**")
                st.markdown("---")
        else:
            st.error("City not found or API error. Please try again.")

if __name__ == "__main__":
    main()
