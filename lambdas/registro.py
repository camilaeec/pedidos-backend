import json
import boto3
import uuid
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ORDERS_TABLE'])
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    print("Evento Registro:", json.dumps(event))
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validar campos
        required_fields = ['storeId', 'client', 'address', 'total', 'items']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Campo faltante: {field}'})
                }
        
        # Crear pedido con single table design
        order_id = f"ORD-{str(uuid.uuid4())[:8].upper()}"
        timestamp = datetime.now().isoformat()
        
        pedido = {
            'PK': f"TENANT#kfc#ORDER#{order_id}",
            'SK': 'METADATA',
            'orderId': order_id,
            'storeId': body['storeId'],
            'client': body['client'],
            'address': body['address'],
            'total': float(body['total']),
            'status': 'CREATED',
            'items': body['items'],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Guardar en DynamoDB
        table.put_item(Item=pedido)
        
        # Enviar a SQS
        sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE'],
            MessageBody=json.dumps({
                'action': 'PROCESS_ORDER',
                'orderId': order_id,
                'pedido': pedido
            })
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Pedido registrado exitosamente',
                'orderId': order_id,
                'status': 'CREATED'
            })
        }
        
    except Exception as e:
        print("Error en registro:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }