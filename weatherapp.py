from flask import Flask, render_template, request
import requests

weatherapp = Flask(__name__)

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        description = weather_data["description"]
        return {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "description": description
        }
    else:
        return None

@weatherapp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        api_key = "692f38118b8294e655d01c4e1d08efd1"
        weather_data = get_weather(api_key, city)
        if weather_data:
            return render_template("weatherapp.html", weather_data=weather_data)
        else:
            return render_template("weatherapp.html", error="City not found!")

    return render_template("weatherapp.html", weather_data=None, error=None)

if __name__ == "__main__":
    weatherapp.run(debug=True)
