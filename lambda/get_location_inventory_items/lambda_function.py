import boto3
import json

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get the location_id from the path parameters
    if 'pathParameters' not in event or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    loc_id = event['pathParameters']['location_id']

    # Query the Global Secondary Index (GSI)
    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName='InventoryGSI',
            KeyConditionExpression='location_id = :l',
            ExpressionAttributeValues={
                ':l': {'S': str(loc_id)}
            }
        )
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }