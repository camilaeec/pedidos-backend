import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PEDIDOS_TABLE'])

def lambda_handler(event, context):
    print("Evento Status:", json.dumps(event))
    
    # Obtener orderId de query parameters
    order_id = event.get('queryStringParameters', {}).get('orderId')
    
    if not order_id:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Parámetro orderId requerido'})
        }
    
    try:
        # Obtener pedido de DynamoDB
        response = table.get_item(Key={'id': order_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Pedido no encontrado'})
            }
        
        pedido = response['Item']
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(pedido)
        }
        
    except Exception as e:
        print("Error en status:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Error al obtener pedido'})
        }
