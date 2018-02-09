API_KEY = 'API_KEY'
SLACK_TOKEN = 'SLACK_TOKEN'

 # Responses
SUCCESS = {'message': 'Success'} # 200
SLACK_ID_NOT_FOUND = {'message': 'Slack ID Not Found'} # 404
WRONG_CHECK_IN_CODE = {'message': 'Wrong Check In Code'} # 403
MISSING_FIELDS = {'message': 'Missing Fields'} # 400
BAD_API_KEY = {'message': 'Bad API Key'} # 401
NOT_AN_ADMIN = {'message': 'Not an Admin in Slack team'} # 401