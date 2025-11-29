import json
import boto3
import uuid
from datetime import datetime
import os
from common.db import pedidos_table
from common.response import json_response

sqs = boto3.resource('sqs')

def lambda_handler(event, context):
    print("Evento Registro:", json.dumps(event))
    try:
        body = json.loads(event.get('body', '{}'))
        required_fields = ['storeId', 'client', 'address', 'total', 'items']
        for field in required_fields:
            if field not in body:
                return json_response({'error': f'Campo faltante: {field}'}, status=400)

        order_id = f"ORD-{str(uuid.uuid4())[:8].upper()}"
        timestamp = datetime.utcnow().isoformat()

        pedido = {
            'id': order_id,
            'orderId': order_id,
            'storeId': body['storeId'],
            'client': body['client'],
            'address': body['address'],
            'total': float(body['total']),
            'status': 'PENDING',
            'items': body['items'],
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        # Guardar en DynamoDB
        table = pedidos_table()
        table.put_item(Item=pedido)

        # Enviar a SQS (por nombre de cola)
        queue = sqs.get_queue_by_name(QueueName=os.environ['SQS_QUEUE'])
        queue.send_message(MessageBody=json.dumps({
            'action': 'PROCESS_ORDER',
            'orderId': order_id,
            'pedido': pedido
        }))

        return json_response({'message': 'Pedido registrado exitosamente', 'orderId': order_id, 'status': 'PENDING'})
    except Exception as e:
        print("Error en registro:", str(e))
        return json_response({'error': f'Error interno: {str(e)}'}, status=500)
