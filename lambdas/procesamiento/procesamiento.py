import json
import os
from datetime import datetime
from common.db import pedidos_table
from common.response import json_response

def lambda_handler(event, context):
    print("Evento Procesamiento SQS:", json.dumps(event))
    table = pedidos_table()
    for record in event.get('Records', []):
        try:
            message = json.loads(record['body'])
            order_id = message.get('orderId')
            print(f"Procesando pedido: {order_id}")

            # Actualizar estado a PROCESSING
            table.update_item(
                Key={'id': order_id},
                UpdateExpression='SET #s = :new_status, updatedAt = :now',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={
                    ':new_status': 'PROCESSING',
                    ':now': datetime.utcnow().isoformat()
                }
            )
            print(f"Pedido {order_id} marcado como PROCESSING")
            # NOTA: aquí podrías lanzar Step Functions (pero no es tu alcance).
        except Exception as e:
            print(f"Error procesando mensaje: {str(e)}")
            # SQS reintenta y al tercer intento DLQ recogerá el mensaje
    return json_response({'message': 'Procesamiento completado'})
