import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['MENU_TABLE'])

# Datos del menú KFC
menu_data = [
    {
        "productId": "MEGA-DELIVERY-6",
        "name": "Mega Delivery - 6 Piezas",
        "description": "6 Piezas de Pollo y 1 Papa Familiar",
        "originalPrice": 59.30,
        "discountPrice": 39.90,
        "discountPercent": 32,
        "category": "megas",
        "store": "KFC",
        "image": "https://bucket-s3-imagenes.s3.amazonaws.com/mega-delivery-6.jpg"
    },
    {
        "productId": "WINGS-KRUNCH-18",
        "name": "Wings & Krunch: 18 Hot Wings",
        "description": "18 Hot Wings y 1 Complemento Familiar",
        "originalPrice": 63.20,
        "discountPrice": 37.90,
        "discountPercent": 40,
        "category": "promociones",
        "store": "KFC",
        "image": "https://bucket-s3-imagenes.s3.amazonaws.com/wings-krunch-18.jpg"
    },
    {
        "productId": "MEGA-PROMO-8",
        "name": "Mega Promo - 8 Piezas",
        "description": "8 Piezas de Pollo y 1 Papa Familiar",
        "originalPrice": 75.10,
        "discountPrice": 49.90,
        "discountPercent": 33,
        "category": "megas",
        "store": "KFC",
        "image": "https://bucket-s3-imagenes.s3.amazonaws.com/mega-promo-8.jpg"
    }
    # ... agregar todos los productos del menú
]

def lambda_handler(event, context):
    print("Evento Menu:", json.dumps(event))
    
    try:
        # Obtener store de query parameters (multitenancy)
        store = event.get('queryStringParameters', {}).get('store', 'KFC')
        
        # Si es la primera vez, poblar la tabla
        if event.get('queryStringParameters', {}).get('init') == 'true':
            with table.batch_writer() as batch:
                for item in menu_data:
                    batch.put_item(Item=item)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'Menú inicializado'})
            }
        
        # Obtener menú filtrado por store
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('store').eq(store)
        )
        
        items = response.get('Items', [])
        
        # Filtrar por categoría si se especifica
        category = event.get('queryStringParameters', {}).get('category')
        if category:
            items = [item for item in items if item.get('category') == category]
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'store': store,
                'menu': items
            })
        }
        
    except Exception as e:
        print("Error en menu:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Error al obtener menú'})
        }
