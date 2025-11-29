import json
from common.response import json_response

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    # En un caso real: validar, hashear password, guardar en Users DynamoDB
    if not body.get('username'):
        return json_response({'error': 'username es requerido'}, status=400)
    return json_response({'message': 'Usuario registrado (mock)', 'user': {'username': body.get('username')}})
