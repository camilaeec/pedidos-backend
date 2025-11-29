import json
import os
import boto3
from boto3.dynamodb.conditions import Attr
from common.db import menu_table
from common.response import json_response

def lambda_handler(event, context):
    print("Evento Menu:", json.dumps(event))
    try:
        params = event.get('queryStringParameters') or {}
        store = params.get('store', 'KFC')
        category = params.get('category')

        table = menu_table()

        # Si solicitan init por query param, poblar con el JSON (dev)
        if params.get('init') == 'true':
            # inicializar desde file
            try:
                with open('menu_data.json', 'r', encoding='utf-8') as f:
                    menu_data = json.load(f)
            except Exception:
                menu_data = []
            with table.batch_writer() as batch:
                for item in menu_data:
                    product = {
                        'productId': item.get('id') or item.get('productId'),
                        'name': item.get('name'),
                        'description': item.get('description'),
                        'originalPrice': item.get('originalPrice', item.get('price')),
                        'discountPrice': item.get('price'),
                        'category': item.get('category'),
                        'store': item.get('store', store),
                        'image': item.get('image', '')
                    }
                    batch.put_item(Item=product)
            return json_response({'message': 'Menú inicializado'})

        # Query por store usando scan + filter (para simplicidad)
        response = table.scan(
            FilterExpression=Attr('store').eq(store)
        )
        items = response.get('Items', [])

        if category:
            items = [i for i in items if i.get('category') == category]

        return json_response({'store': store, 'menu': items})
    except Exception as e:
        print("Error en menu:", str(e))
        return json_response({'error': 'Error al obtener menú'}, status=500)
