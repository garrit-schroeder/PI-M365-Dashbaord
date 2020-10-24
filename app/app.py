import os

import babel as babel
from flask import Flask
from flask import render_template
from pip._vendor import requests
from datetime import date, datetime

template_dir = os.path.abspath('templates')
app = Flask(__name__)


@app.template_filter('strftime')
def format_datetime(value):
    date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f0')
    return date.strftime("%H:%M")


@app.route('/')
def hello_world():
    today = datetime.now()
    json = {
        "calendar_filter_start": today.strftime("%Y-%m-23T00:00"),  # %Y-%m-%dT%H:%M
        "calendar_filter_end": today.strftime("%Y-%m-23T23:59")
    }
    res = requests.post(os.environ.get("LOGIC_APP_URL"), json=json)
    data = res.json()
    if res.status_code == 200:
        return render_template('index.html', data=res.json())
    else:
        return "error calling azure logic app"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
