import random
import string


def generate_check_in_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))


def toggle_active_delete(db, check_in_code, active, delete=False):
    events = db.events
    events.update_one({'check_in_code': check_in_code},
                      {"$set": {'active': active, 'deleted': delete}})

    update_scores(db, check_in_code, delete)


def update_scores(db, check_in_code, delete=False):
    # Check if the user was to that event
    users_collection = db.users
    users = db.users.find({'events': check_in_code})
    event = db.events.find_one({'check_in_code': check_in_code})
    score = event.get('weight')

    for user in users:
        if delete:
            users_collection.update_one({'slack_id': user.get('slack_id')}, {
                '$set': {'score': (user.get('score') - score)}})
        else:
            print(score)
            users_collection.update_one({'slack_id': user.get('slack_id')}, {
                '$set': {'score': (user.get('score') + score)}})
