from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from verification import verify_user, verify_api_key, verify_admin
from utils import generate_check_in_code, toggle_active_delete
from config import SUCCESS, SLACK_ID_NOT_FOUND, WRONG_CHECK_IN_CODE, MISSING_FIELDS

app = Flask(__name__)

client = MongoClient()
db = client.chicken

@app.route('/')
def index():
    return "hello world"


@app.route('/checkin', methods=['POST'])
@verify_api_key
def check_in():
    check_in_code = request.get_json().get('check_in_code')
    slack_id = request.headers.get('slack_id')

    # First verify the user is valid
    if not verify_user(slack_id):
        return jsonify(SLACK_ID_NOT_FOUND), 404

    # Then verify the event exists and is active
    events = db.events
    event = events.find_one({'check_in_code': check_in_code})

    if event is None or not event.get('active'):
        return jsonify(WRONG_CHECK_IN_CODE), 403

    score = event.get('weight')

    # Then query for the user
    users = db.users
    user = users.find_one({'slack_id': slack_id})

    if user is None:
        user = {
            'slack_id': slack_id,
            'events': [],
            'score': score
        }

        db.users.insert_one(user)

    # If they exist, add this check-in code
    if check_in_code not in user.get('events'):
        new_score = user.get('score') + score
        users.update_one({'slack_id': slack_id}, {
            '$push': {'events': check_in_code}})

        users.update_one({'slack_id': slack_id}, {
                         '$set': {'score': new_score}})

    # Then update the event with the user's slack_id
    if slack_id not in event.get('attendees'):
        events.update_one({'check_in_code': check_in_code}, {
                          '$push': {'attendees': slack_id}})

    return jsonify(SUCCESS), 200


@app.route('/event/new', methods=['POST'])
@verify_api_key
@verify_admin
def start_checkin():
    json = request.get_json()
    name = json.get('name')
    description = json.get('description')
    timestamp = json.get('timestamp')
    weight = json.get('weight')
    slack_id = request.headers.get('slack_id')

    if timestamp is None:
        timestamp = datetime.now()

    if weight is None:
        weight = 1.0

    if name is None or description is None or slack_id is None:
        return jsonify(MISSING_FIELDS), 400

    check_in_code = generate_check_in_code()

    # Create the event and insert it into the database
    event = {
        'name': name,
        'description': description,
        'timestamp': timestamp,
        'weight': weight,
        'slack_id': slack_id,
        'check_in_code': check_in_code,
        'active': True,
        'deleted': False,
        'attendees': []
    }

    events = db.events
    result = events.insert_one(event)

    return jsonify({
        'event_id': str(result.inserted_id),
        'check_in_code': check_in_code
    }), 200


@app.route('/event/list', methods=['GET'])
@verify_api_key
@verify_admin
def list_all_events():
    events = db.events
    all_events = []

    # Serialize the object id
    for event in events.find({'deleted': False}):
        event['_id'] = str(event['_id'])
        all_events.append(event)

    return jsonify({'events': all_events}), 200


@app.route('/event/list/active', methods=['GET'])
@verify_api_key
@verify_admin
def list_active_events():
    events = db.events
    all_events = []

    # Serialize the object id
    for event in events.find({'active': True}):
        event['_id'] = str(event['_id'])
        all_events.append(event)

    return jsonify({'events': all_events}), 200


@app.route('/event/close', methods=['PUT'])
@verify_api_key
@verify_admin
def close_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or event.get('deleted') or not event.get('active'):
        return jsonify(WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=False)

    return jsonify(SUCCESS), 200


@app.route('/event/reopen', methods=['PUT'])
@verify_api_key
@verify_admin
def reactivate_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or event.get('active'):
        return jsonify(WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=True)

    return jsonify(SUCCESS), 200


@app.route('/event/delete', methods=['PUT'])
@verify_api_key
@verify_admin
def delete_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or event.get('deleted'):
        return jsonify(WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=False, delete=True)

    return jsonify(SUCCESS), 200


@app.route('/event/reactivate', methods=['PUT'])
@verify_api_key
@verify_admin
def restore_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or not event.get('active'):
        return jsonify(WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=True, delete=False)

    return jsonify(SUCCESS), 200


# Runs the app (in debug mode)
if __name__ == "__main__":
    app.run(debug=True)
