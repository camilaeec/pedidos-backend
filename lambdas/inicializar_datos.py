import json
from common.db import menu_table, locales_table
from common.response import json_response

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        print(f"⚠ {filename} no encontrado o corrupto")
        return []

def lambda_handler(event, context):
    try:
        # ---- CARGAR MENÚ ----
        menu_items = load_json('menu_data.json')
        if menu_items:
            table = menu_table()
            with table.batch_writer() as batch:
                for item in menu_items:
                    batch.put_item(Item={
                        'productId': item.get('id') or item.get('productId'),
                        'name': item['name'],
                        'description': item['description'],
                        'category': item['category'],
                        'originalPrice': item.get('originalPrice', item['price']),
                        'discountPrice': item['price'],
                        'store': item.get('store', 'KFC'),  
                        "image": item.get('image', '')
                    })

        # ---- CARGAR LOCALES ----
        locales = load_json('locales.json')
        if locales:
            ltable = locales_table()
            with ltable.batch_writer() as batch:
                for loc in locales:
                    batch.put_item(Item=loc)

        return json_response({
            'message': 'Datos inicializados correctamente',
            'menuItems': len(menu_items),
            'locales': len(locales)
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return json_response({'error': str(e)}, status=500)
