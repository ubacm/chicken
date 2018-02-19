# chicken

The check in system for UB ACM events.

## `POST /checkin`

Allows a user to check into an event.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String,
  username: String
}
```

### Response

* Success: Response Code 200
* Failure - Bad API Key: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `GET /event/list`

Shows all events.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200

```node
{
    "events": [
        {
            "_id": String,
            "active": Boolean,
            "attendees": [
                String,
                ...
            ],
            "check_in_code": String,
            "deleted": Boolean,
            "description": String,
            "name": String,
            "slack_id": String,
            "timestamp": String,
            "weight": Integer
        },
        ...
}
```

* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `GET /event/list/active`

Shows all active events.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200

```node
{
    "events": [
        {
            "_id": String,
            "active": Boolean,
            "attendees": [
                String,
                ...
            ],
            "check_in_code": String,
            "deleted": Boolean,
            "description": String,
            "name": String,
            "slack_id": String,
            "timestamp": String,
            "weight": Integer
        },
        ...
}
```

* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `POST /event/new`

Creates a new event.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  name: String,
  description: String,
  timestamp: Long, // Optional, Default: Now
  weight: Float, // Optional, Default: 1.0
}
```

### Response

* Success: Response Code 200

```node
{
  event_id: Integer,
  check_in_code: String
}
```

* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `PUT /event/close`

Closes an event provided with an ID.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200
* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `PUT /event/reopen`

Reopens a previously closed event provided with an ID.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200
* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `PUT /event/delete`

Soft-deletes an event from the database. All check-ins for this event is invalid.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200
* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `PUT /event/reactivate`

Restores a previously deleted event provided with an ID.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  check_in_code: String
}
```

### Response

* Success: Response Code 200
* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `GET /users/scores`

Gets all of the users and their scores (in descending order).

### Request

Just a basic `GET` request will do.

### Response

```node
{
  [
    {
      'username': String,
      'slack_id': String,
      'events': [String, String, ...],
      'score': Integer
    },
  ...
  ]
}
```

## `POST /users/scores/edit`

Add the score passed in to the users current score. So to add pass a positive number and to subtract, send a negative number. The `slack_id` in the header is the admin id and the `slack_id` in the body is for the user that will be updated.

### Request

#### Header

```node
  api_key: String,
  slack_id: String
```

#### Body

```node
{
  score: Float,
  slack_id: String
}
```

### Response

* Success: Response Code 200
* Failure - Missing Fields: Response Code 400
* Failure - Bad API Key: Response Code 401
* Failure - Not an Admin in Slack team: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404

```node
{
  message: String
}
```

## `GET /event/<check_in_code>`

Get details of an event including a list of all the attendees.

### Request

Just a basic `GET` request to this route with the check in code for
the event as a parameter.

### Response

* Success: Response Code 200

```node
{
  event: {
    active: Boolean,
    check_in_code: String,
    deleted: Boolean,
    name: String,
    slack_id: String,
    timestamp: String,
    weight: Integer
  },
  attendees: [String, String, ...],
  count: Integer
}
```

* Failure - Wrong Check In Code: Response Code 403

```node
{
  message: String
}
```
