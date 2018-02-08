# chicken
The check in system for UB ACM events.

## `/checkin`
Allows a user to check into an event.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
```node
{
  check_in_code: String
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

## `/event/list`
Shows all events.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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


## `/event/list/active`
Shows all active events.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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

## `/event/new`
Creates a new event.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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

## `/event/close`
Closes an event provided with an ID.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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


## `/event/reopen`
Reopens an previously closed event provided with an ID.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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

## `/event/delete`
Soft-deletes an event from the database. All check-ins for this event is invalid.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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


## `/event/reactivate`
Restores a previously deleted event provided with an ID.

### Request
##### Header
```node
  api_key: String,
  slack_id: String
```
##### Body
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



