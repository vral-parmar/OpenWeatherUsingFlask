import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def weather_dashboard():
    return render_template('home.html')


@app.route("/results", methods=["POST"])
def render_results():
    zipCode = request.form['zipcode']
    api_key = get_api_key()
    data = get_weather_results(zipCode, api_key)
    temp = "{0:.2f}".format(data['main']['temp'])
    temp_min = "{0:.2f}".format(data['main']['temp_min'])
    temp_max = "{0:.2f}".format(data['main']['temp_max'])
    humidity = "{0:.2f}".format(data['main']['humidity'])
    wind = "{0:.2f}".format(data['wind']['speed'])
    Feels_like = "{0:.2f}".format(data['main']['feels_like'])
    weather = data['weather'][0]['main']
    location = data['name']

    return render_template('results.html', temp=temp,
                           Feels_like=Feels_like,
                           weather=weather,
                           location=location,
                           temp_min=temp_min,
                           temp_max=temp_max,
                           humidity=humidity,
                           wind=wind)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    print(api_url)
    return r.json()


# print(get_weather_results("95129", get_api_key()))

if __name__ == '__main__':
    app.run()
