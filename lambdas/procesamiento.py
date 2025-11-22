import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PEDIDOS_TABLE'])

def lambda_handler(event, context):
    print("Evento Procesamiento SQS:", json.dumps(event))
    
    for record in event['Records']:
        try:
            message = json.loads(record['body'])
            order_id = message['orderId']
            pedido = message['pedido']
            
            print(f"Procesando pedido: {order_id}")
            
            # Simular procesamiento - actualizar estado
            table.update_item(
                Key={'id': order_id},
                UpdateExpression='SET #status = :new_status, updatedAt = :now',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':new_status': 'PROCESSING',
                    ':now': json.loads(json.dumps(datetime.now().isoformat()))
                }
            )
            
            print(f"Pedido {order_id} marcado como PROCESSING")
            
            # Aquí luego iniciarás Step Functions
            # Por ahora solo marcamos como procesado
            
        except Exception as e:
            print(f"Error procesando mensaje {record['messageId']}: {str(e)}")
            # El mensaje irá a DLQ después de 3 intentos
    
    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento SQS completado')
    }
