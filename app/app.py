from flask import Flask, render_template, request  # Importer Flask og verktøy for HTML og skjemaer
import requests   # Bibliotek for å sende HTTP-forespørsler til APIer
from datetime import datetime

app = Flask(__name__)
API_KEY = "f605f7884d50ce3f7697a22d5f5b9c5e"  # Din API-nøkkel til OpenWeatherMap

@app.route("/", methods=["GET", "POST"])  # Definerer startsiden "/" og tillater både å åpne siden (GET) og sende skjema (POST)
def home():
    weather = None  # Starter med ingen værdata, vil fylles hvis brukeren sender inn by
    if request.method == "POST":
        city = request.form.get("city").strip()  # Henter bynavnet fra input-feltet i skjemaet og fjerner mellomrom

        #  Spesiell sjekk for "fyrverkeri"
        if city.lower() == "fyrverkeri":
            weather = {
                "city": city,
                "special": "firework"  # Flag for HTML/JS
            }
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=no"
            response = requests.get(url)  # Sender forespørsel til APIet og lagrer svaret

            if response.status_code == 200:
                data = response.json()

                local_time = datetime.utcfromtimestamp(
                    data["dt"] + data["timezone"]
                ).hour

                is_night = local_time >= 20 or local_time < 6

                # Lagre relevant data i weather for å sende til HTML
                weather = {
                    "city": city,
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "is_night": is_night,
                    "wind": data["wind"]["speed"]
                }
            else:
                weather = {"error": "Kunne ikke hente været."}

    return render_template("index.html", weather=weather)


if __name__ == "__main__":  # Kjører appen hvis filen kjøres direkte
    app.run(debug=True)  # debug=True gir feilmeldinger og automatisk reload ved endringer
