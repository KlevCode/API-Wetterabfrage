import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Eingabedaten
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("API KEY EINTRAGEN")
account_sid = "ACCOUNT SID DES EIGENEN KONTO"
auth_token = os.environ.get("AUTH_TOKEN")

# Standortangaben unter Ausschluss der current,- minütigen,- und täglichen Daten
weather_params = {
    "lat": "51.21",
    "lon": "8.556",
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

# API-Datenabfrage über requests-Modul, Ausgabe der Daten im 12-Stundenformat in JSON

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]


# Funktion zur Codeabfrage

will_snow = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if 622 > int(condition_code) > 600:
        will_snow = True

if will_snow:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Schneefall in Winterberg vorhergesagt!",
        from_="TWILIO VIRTUAL NUMBER",
        to="EIGENE NUMMER"
    )
    print(message.status)
