import os
from datetime import datetime, timedelta, timezone

import pytz
import tzlocal as tzlocal
from flask import Flask
from flask import render_template
from pip._vendor import requests
from pip._vendor.toml import tz

template_dir = os.path.abspath('templates')
app = Flask(__name__)
AZURE_RESPONSE = None


def get_azure_information():
    global AZURE_RESPONSE
    if AZURE_RESPONSE is None or AZURE_RESPONSE['date'] < datetime.utcnow() + timedelta(minutes=-5):
        today = datetime.now()
        json = {
            "calendar_filter_start": today.strftime("%Y-%m-%dT%H:%M"),
            "calendar_filter_end": today.strftime("%Y-%m-%dT23:59")
        }
        res = requests.post(os.environ.get("LOGIC_APP_URL"), json=json)
        data = res.json()
        data['calendar']['value'] = sorted(data['calendar']['value'], key=lambda event: event['start'])
        data['todos'] = list(filter(lambda x: not x['status'] == 'completed', data['todos']))
        data['planner']['value'] = list(filter(lambda x: x['completedDateTime'] is not None, data['planner']['value']))
        AZURE_RESPONSE = {
            "date": datetime.utcnow(),
            "data": data,
            "cached": False
        }
        return AZURE_RESPONSE
    else:
        AZURE_RESPONSE['cached'] = True
        return AZURE_RESPONSE


get_azure_information()


@app.template_filter('strftime')
def format_datetime(value):
    local_timezone = pytz.timezone("Europe/Berlin")
    utc_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f0')
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc)
    local_datetime = local_datetime.astimezone(local_timezone)
    return local_datetime.strftime("%H:%M")


@app.route('/')
def hello_world():
    if os.environ.get("LOGIC_APP_URL") is None:
        return "environment variable LOGIC_APP_URL is not set"
    data = get_azure_information()
    print("cached = " + str(data['cached']))
    return render_template('index.html', data=data['data'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
