import json
import boto3
import uuid
from decimal import Decimal

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except Exception:
        return {'statusCode': 400, 'body': json.dumps("Bad request. Provide data.")}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    unique_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'location_id': str(data['location_id']),
                'item_name': str(data['item_name']),
                'item_description': str(data['item_description']),
                'item_qty': int(data['item_qty']),
                'item_price': Decimal(str(data['item_price']))
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}