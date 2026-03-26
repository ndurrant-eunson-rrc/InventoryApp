import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {'statusCode': 400, 'body': json.dumps("Missing 'id' parameter")}

    key_value = event['pathParameters']['id']
    key = {'id': {'S': key_value}}

    try:
        lookup = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression='item_id = :iid',
            ExpressionAttributeValues={':iid': {'S': str(key_value)}}
        )

        items = lookup.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps("Item not found.")}

        loc_id = items[0]['location_id']['S']

        dynamo_client.delete_item(
            TableName=table_name, 
            Key={
                'item_id': {'S': str(key_value)},
                'location_id': {'S': loc_id}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {key_value} deleted successfully.")
        }
        
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}