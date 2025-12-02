from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import requests
from collections import Counter
import sqlite3
import json   # ← IMPORT PYTHON JSON (important !)

app = Flask(__name__)


@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)


@app.route("/contact/")
def contact_page():
    return render_template("contact.html")


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route('/api/commits-data')
def commits_data():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers).json()

    # Vérifier si GitHub a renvoyé une erreur
    if isinstance(response, dict) and "message" in response:
        return jsonify([["Minute", "Commits"], [0, 0]])

    minutes_list = []

    for commit in response:
        date_str = commit["commit"]["author"]["date"]
        date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minutes_list.append(date_object.minute)

    counts = Counter(minutes_list)

    data = [["Minute", "Commits"]]
    for minute, nb in sorted(counts.items()):
        data.append([minute, nb])

    return jsonify(data)


@app.route('/commits/')
def commits_chart():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
