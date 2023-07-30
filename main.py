import os
import time
from dotenv import load_dotenv
import requests
import datetime
from twilio.rest import Client

load_dotenv()

twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

ow_api_key = os.getenv('OW_API_KEY')

ow_endpoint = "https://api.openweathermap.org/data/2.5/weather"
current_hour = datetime.datetime.now().time().hour
parameters = {
    "lat": "35.7219",
    "lon": "51.3347",
    "appid": ow_api_key
}

while 7 < current_hour < 19:
    response = requests.get(ow_endpoint, params=parameters)
    response.raise_for_status()
    weather_data = response.json()['weather']
    weather_id = weather_data[0]['id']

    if weather_id <= 700:
        client = Client(twilio_account_sid, twilio_auth_token)
        message = client.messages.create(
            from_=os.getenv('FROM_NUMBER'),
            body='you need an umbrella today',
            to=os.getenv('TO_NUMBER')
        )
        print(message.sid)

    else:
        client = Client(twilio_account_sid, twilio_auth_token)
        message = client.messages.create(
            from_=os.getenv('FROM_NUMBER'),
            body='you dont need an umbrella today',
            to=os.getenv('TO_NUMBER')
        )
        print(message.sid)

    # time.sleep(3600)
    time.sleep(30)
    current_hour = datetime.datetime.now().time().hour
