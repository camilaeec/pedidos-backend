import json

def lambda_handler(event, context):
    print("Evento Autorizador:", json.dumps(event))
    
    # Autorización simple para desarrollo
    token = event.get('headers', {}).get('Authorization', '')
    
    if token and ('Bearer demo-token' in token or 'demo-token' in token):
        return {
            'principalId': 'user123',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': event['methodArn']
                    }
                ]
            },
            'context': {
                'user': 'demo-user'
            }
        }
    
    # Denegar por defecto
    raise Exception('Unauthorized')
