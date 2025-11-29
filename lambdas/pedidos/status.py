import json
import os
from common.db import pedidos_table
from common.response import json_response

def lambda_handler(event, context):
    print("Evento Status:", json.dumps(event))
    params = event.get('queryStringParameters') or {}
    order_id = params.get('orderId')
    if not order_id:
        return json_response({'error': 'Parámetro orderId requerido'}, status=400)
    try:
        table = pedidos_table()
        response = table.get_item(Key={'id': order_id})
        if 'Item' not in response:
            return json_response({'error': 'Pedido no encontrado'}, status=404)
        return json_response(response['Item'])
    except Exception as e:
        print("Error en status:", str(e))
        return json_response({'error': 'Error al obtener pedido'}, status=500)
