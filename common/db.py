import os
import boto3

dynamodb = boto3.resource('dynamodb')
PEDIDOS_TABLE = os.environ.get('PEDIDOS_TABLE')
MENU_TABLE = os.environ.get('MENU_TABLE')
LOCALES_TABLE = os.environ.get('LOCALES_TABLE')

def pedidos_table():
    return dynamodb.Table(PEDIDOS_TABLE)

def menu_table():
    return dynamodb.Table(MENU_TABLE)

def locales_table():
    return dynamodb.Table(LOCALES_TABLE)
