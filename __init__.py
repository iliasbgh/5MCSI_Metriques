from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

# -----------------------------------------------------------
# PAGE D'ACCUEIL
# -----------------------------------------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')  # tu dois mettre ton nom dans hello.html


# -----------------------------------------------------------
# EXERCICE 2 : ROUTE /contact/
# -----------------------------------------------------------
@app.route("/contact/")
def MaPremiereAPI():
    # Pour l'exercice 5 tu pointeras vers un template HTML
    return "<h2>Ma page de contact</h2>"


# -----------------------------------------------------------
# EXERCICE 3 : ROUTE /tawarano/
# -----------------------------------------------------------
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


# -----------------------------------------------------------
# EXERCICE 3 BIS : AFFICHAGE D'UN FICHIER HTML
# -----------------------------------------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# -----------------------------------------------------------
# EXERCICE 4 : HISTOGRAMME /histogramme/
# -----------------------------------------------------------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


# -----------------------------------------------------------
# EXERCICE 6 : COMMITS GITHUB /commits/
# -----------------------------------------------------------
@app.route("/commits/")
def commits():
    response = urlopen("https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits")
    data = json.loads(response.read().decode("utf-8"))

    results = []
    for commit in data:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute_value = date_obj.minute
            results.append({"minute": minute_value})

    return jsonify(results=results)


# -----------------------------------------------------------
# ROUTE ANNEXE FOURNIE DANS L’ENONCÉ
# -----------------------------------------------------------
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


# -----------------------------------------------------------
# LANCEMENT DE L'APPLICATION
# -----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
