import requests
import json
import datetime
import smtplib
from QuoteSender import today_quote
import os


def convert_time(time_f):
    utc_time = datetime.datetime.utcfromtimestamp(time_f)
    utc = [utc_time.hour, utc_time.minute]
    ist = [(utc[0] + 5 + (utc[1] + 30) // 60) % 24, (utc[1] + 30) % 60]
    if 0 <= ist[0] <= 11:
        sun = "AM"
    else:
        sun = "PM"
        if ist[0] > 12:
            ist[0] -= 12
    return f"{ist[0]:02d}:{ist[1]:02d} {sun}"


def send_mail():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs="sahilkhanvns1228@gmail.com",
        msg=f"Subject:Weather Predictions\n\n{today_msg}"
    )
    connection.close()


MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
MY_API_KEY = os.getenv("MY_API_KEY")

# -- Noida
MY_LAT = 28.475628
MY_LNG = 77.475332

API_KEY = MY_API_KEY
api_params = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": API_KEY,
    "units": "metric"
    # "exclude": "current,minutely,daily"
}
api_endpoint = f"https://api.openweathermap.org/data/2.5/onecall"

response = requests.get(url=api_endpoint, params=api_params)
data = response.json()
with open("weather_data.json", mode="w") as file:
    json.dump(data, file, indent=4)

# list_weather = []
# for i in range(12):
#     list_weather.append(data["hourly"][i]["weather"][0]["id"])
# print(list_weather)

today_data = data["daily"][0]

time_sunrise = convert_time(today_data["sunrise"])
time_sunset = convert_time(today_data["sunset"])

temp_morning = round(today_data["temp"]["morn"])
temp_noon = round(today_data["temp"]["day"])
temp_evening = round(today_data["temp"]["eve"])
temp_night = round(today_data["temp"]["night"])

weather_condition = today_data["weather"][0]["description"]
weather_condition = weather_condition.title()

quote = today_quote()

today_msg = f"Sunrise Time:- {time_sunrise}\nSunset Time:- {time_sunset}\n\n" \
            f"Morning Temperature:- {temp_morning} C\n" \
            f"Noon Temperature:- {temp_noon} C\nEvening Temperature:- {temp_evening} C\n" \
            f"Night Temperature:- {temp_night} C\n\n" \
            f"Weather Condition:- {weather_condition}\n\n" \
            f"{quote[0]}'s QUOTE:\n{quote[1]}\n\n" \
            f"Have a Nice Day."

send_mail()
