from flask import request
from app.config import *
from app.validator import validate_request
from app import flask_front
from time import sleep
import requests
import threading


@flask_front.route('/', methods=['POST'])
def index():
    request_info = request.json
    data = validate_request(request_info)
    if data is None:
        return {"ok": True}
    return data


def set_webhook():
    requests.post(SET_WEBHOOK_URL, DATA)


if __name__ == '__main__':
    set_webhook()
    flask_front.run(host='0.0.0.0', port=5001)
