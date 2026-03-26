import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {'statusCode': 400, 'body': json.dumps("Missing id")}

    key_value = event['pathParameters']['id']

    try:
        response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression='item_id = :iid',
            ExpressionAttributeValues={':iid': {'S': str(key_value)}}
        )
        items = response.get('Items', [])

        if not items:
            return {'statusCode': 404, 'body': json.dumps('Item not found')}

        return {'statusCode': 200, 'body': json.dumps(items[0], default=str)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}