from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient
from datetime import datetime
from verification import verify_user, verify_api_key, verify_admin
from utils import generate_check_in_code, toggle_active_delete
import config as con
import os

app = Flask(__name__)

client = MongoClient(con.MONGO_URI)
db = client.chicken


@app.route('/')
def index():
    return redirect('/users/scores')


@app.route('/checkin', methods=['POST'])
@verify_api_key
def check_in():
    check_in_code = request.get_json().get('check_in_code')
    slack_id = request.headers.get('slack_id')
    username = request.get_json().get('username')

    if username is None:
        return jsonify(con.MISSING_FIELDS), 400

    # First verify the user is valid
    if not verify_user(slack_id):
        return jsonify(con.SLACK_ID_NOT_FOUND), 404

    # Then verify the event exists and is active
    events = db.events
    event = events.find_one({'check_in_code': check_in_code})

    if event is None or not event.get('active'):
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    # Then query for the user
    users = db.users
    user = users.find_one({'slack_id': slack_id})

    if user is None:
        user = {
            'username': username,
            'slack_id': slack_id,
            'events': [],
            'score': 0
        }
        db.users.insert_one(user)

    # If they exist, add this check-in code
    if check_in_code not in user.get('events'):
        new_score = user.get('score') + event.get('weight')
        users.update_one({'slack_id': slack_id}, {
            '$push': {'events': check_in_code}})

        users.update_one({'slack_id': slack_id}, {
                         '$set': {'score': new_score}})

    # Then update the event with the user's slack_id
    if slack_id not in event.get('attendees'):
        events.update_one({'check_in_code': check_in_code}, {
                          '$push': {'attendees': slack_id}})

    return jsonify(con.SUCCESS), 200


@app.route('/event/new', methods=['POST'])
@verify_api_key
@verify_admin
def start_checkin():
    json = request.get_json()
    name = json.get('name')
    timestamp = json.get('timestamp')
    weight = json.get('weight')
    slack_id = request.headers.get('slack_id')

    if timestamp is None:
        timestamp = datetime.now()

    if weight is None:
        weight = 1.0

    if name is None or slack_id is None:
        return jsonify(con.MISSING_FIELDS), 400

    check_in_code = generate_check_in_code()
    events = db.events

    while True:
        event_in_db = events.find_one({'check_in_code': check_in_code})
        if event_in_db is not None:
            check_in_code = generate_check_in_code()
        else:
            break

    # Create the event and insert it into the database
    event = {
        'name': name,
        'timestamp': timestamp,
        'weight': weight,
        'slack_id': slack_id,
        'check_in_code': check_in_code,
        'active': True,
        'deleted': False,
        'attendees': []
    }

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
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=False)

    return jsonify(con.SUCCESS), 200


@app.route('/event/reopen', methods=['PUT'])
@verify_api_key
@verify_admin
def reactivate_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or event.get('active'):
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=True)

    return jsonify(con.SUCCESS), 200


@app.route('/event/delete', methods=['PUT'])
@verify_api_key
@verify_admin
def delete_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or event.get('deleted'):
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=False, delete=True)

    return jsonify(con.SUCCESS), 200


@app.route('/event/reactivate', methods=['PUT'])
@verify_api_key
@verify_admin
def restore_event():
    check_in_code = request.get_json().get('check_in_code')
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None or not event.get('deleted'):
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    toggle_active_delete(db, check_in_code, active=True, delete=False)

    return jsonify(con.SUCCESS), 200


@app.route('/score', methods=['GET'])
@verify_api_key
def get_score():
    slack_id = request.headers.get('slack_id')

    # verify this is a slack user
    if not verify_user(slack_id):
        return jsonify(con.SLACK_ID_NOT_FOUND), 404

    # check if the user is in db, add if not
    user = db.users.find_one({'slack_id': slack_id})

    if user is None:
        return jsonify({'score': 0})

    return jsonify({'score': user.get('score')})


@app.route('/users/scores', methods=['GET'])
def get_all_scores():
    users = db.users.find({})
    users = sorted(users, key=lambda x: x['score'], reverse=True)

    for i in range(0, len(users)):
        users[i].pop('_id', None)

    return jsonify(users)


@app.route('/users/scores/edit', methods=['POST'])
@verify_api_key
@verify_admin
def edit_score():
    slack_id = request.get_json().get('slack_id')
    score = request.get_json().get('score')

    if score is None:
        return jsonify(con.MISSING_FIELDS), 400

    # verify this is a slack user
    if not verify_user(slack_id):
        return jsonify(con.SLACK_ID_NOT_FOUND), 404

    user = db.users.find_one({'slack_id': slack_id})

    updated_score = user.get('score') + request.get_json().get('score')

    if user is not None:
        db.users.update_one({'slack_id': slack_id}, {
                            '$set': {'score': updated_score}})
        return jsonify(con.SUCCESS), 200

    return jsonify(con.SLACK_ID_NOT_FOUND), 404


@app.route('/events/<check_in_code>', methods=['GET'])
def view_attendees(check_in_code):
    event = db.events.find_one({'check_in_code': check_in_code})

    if event is None:
        return jsonify(con.WRONG_CHECK_IN_CODE), 403

    event.pop('_id', None)

    users = []

    if event is not None:
        for attendee in event.get('attendees'):
            user = db.users.find_one({'slack_id': attendee})
            users.append(user.get('username'))

    event.pop('attendees', None)

    return jsonify({
        "event": event,
        "attendees": users,
        "count": len(users)
    })


# Runs the app
if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)), debug=True)
