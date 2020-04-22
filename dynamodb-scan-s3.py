from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
s3_client = boto3.client('s3')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('your-dynamodb-table')

    fe = Key('field-dynamodb').begins_with('a')

    response = table.scan(
        FilterExpression=fe,
        )

    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=fe
            )

    for i in response['Items']:
        json_file_name = i['timestamp']
        s3_client.put_object(Bucket = 'yourbucket', Key = json_file_name, Body = (json.dumps(i, indent=4, cls=DecimalEncoder)), ServerSideEncryption = "aws:kms")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
        }
