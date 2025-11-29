import json
from common.response import json_response

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    username = body.get('username')
    password = body.get('password')
    if username == 'demo' and password == 'demo':
        return json_response({'token': 'demo-token', 'user': {'username': 'demo'}})
    return json_response({'error': 'Credenciales invalidas'}, status=401)
