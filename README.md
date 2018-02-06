# chicken
The check in system for UB ACM events.

## `/checkin`
Allows a user to check into an event.

### Request
```node
{
  api_key: String,
  check_in_code: String,
  slack_id: String
}
```
### Response
* Success: Response Code 200
* Failure - Wrong API Key: Response Code 401
* Failure - Wrong Check In Code: Response Code 403
* Failure - Slack ID Not Found: Response Code 404
```node
{
  message: String
}
```

## `/event/delete`
Soft-deletes an event from the database. All check-ins for this event is invalid.

## `/event/list`
Shows all events.

## `/event/list/active`
Shows all active events.

## `/event/new`
Creates a new event, and provides a 

### Request
```node
{
  api_key: String,
  name: String,
  description: String,
  timestamp: Long, // Optional, Default: Now
  weight: Float, // Optional, Default: 1.0
  slack_id: String
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

* Failure - Wrong API Key: Response Code 401
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
