from flask import request, jsonify
from functools import wraps
import requests
from config import SLACK_TOKEN, API_KEY


def verify_user(slack_id):
    url = 'https://slack.com/api/users.info?user=%s&token=%s' % (
        slack_id, SLACK_TOKEN)

    response = requests.get(url)
    is_user = response.json().get('ok')

    return True if is_user else False


def verify_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        api_key = request.headers.get('api_key')

        if api_key is None or api_key != API_KEY:
            return jsonify({'message': 'Bad API Key'}), 401

        return f(*args, **kws)
    return decorated_function


def verify_admin(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        slack_id = request.headers.get('slack_id')

        if not verify_user(slack_id):
            return jsonify({'message': 'Slack ID Not Found'}), 404

        base_url = 'https://slack.com/api/users.info?user=%s&token=%s' % (
            slack_id, SLACK_TOKEN)

        response = requests.get(base_url)
        validated = response.json().get('user').get('is_admin')

        if not validated:
            return jsonify({'message': 'Not an Admin in Slack team'}), 401

        return f(*args, **kws)

    return decorated_function
