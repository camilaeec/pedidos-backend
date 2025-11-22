import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
menu_table = dynamodb.Table(os.environ['MENU_TABLE'])
locales_table = dynamodb.Table(os.environ['LOCALES_TABLE'])

def load_menu_from_json():
    """Carga el menú desde el archivo JSON"""
    try:
        # En Lambda, los archivos están en el directorio raíz
        with open('menu_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("menu_data.json no encontrado, usando datos por defecto")
        return get_default_menu()

def get_default_menu():
    """Menú por defecto si no existe el JSON"""
    return [
        {
            "id": "promo-mega-delivery-6p",
            "name": "Mega Delivery - 6 Piezas",
            "description": "6 Piezas de Pollo y 1 Papa Familiar",
            "price": 39.90,
            "category": "promos",
            "originalPrice": 59.30,
            "discountPercent": 32,
            "image": "/images/mega-delivery-6.jpg"
        }
        # ... algunos productos de ejemplo
    ]

def lambda_handler(event, context):
    print("Inicializando datos KFC...")
    
    try:
        # 1. Cargar menú desde JSON
        menu_json = load_menu_from_json()
        
        # 2. Transformar a formato DynamoDB
        menu_items = []
        for item in menu_json:
            menu_items.append({
                "PK": f"TENANT#kfc#PRODUCT#{item['id']}",
                "SK": "METADATA",
                "productId": item['id'],
                "name": item['name'],
                "description": item['description'],
                "originalPrice": item.get('originalPrice', item['price']),
                "discountPrice": item['price'],
                "discountPercent": item.get('discountPercent', 0),
                "category": item['category'],
                "image": item.get('image', '/images/placeholder.jpg'),
                "available": True
            })
        
        # 3. Poblar locales (puedes hacer lo mismo con un locales.json si quieres)
        locales_items = [
            {
                "storeId": "KFC-003",
                "name": "KFC 003 - AVIACION", 
                "address": "AV. AVIACION NRO. 2798, SAN BORJA, LIMA",
                "city": "LIMA",
                "district": "SAN BORJA",
                "active": True
            }
            # ... más locales
        ]
        
        # 4. Insertar en DynamoDB
        with menu_table.batch_writer() as batch:
            for item in menu_items:
                batch.put_item(Item=item)
        
        with locales_table.batch_writer() as batch:
            for item in locales_items:
                batch.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Datos KFC inicializados exitosamente',
                'menuItems': len(menu_items),
                'locales': len(locales_items)
            })
        }
        
    except Exception as e:
        print("Error inicializando datos:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Error inicializando datos: {str(e)}'})
        }