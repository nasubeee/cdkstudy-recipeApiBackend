from cmath import cos
import boto3
import logging
import datetime
import json
import os
import traceback

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.setLevel(logging.ERROR)

# Create dynamodb client
dynamo_client = boto3.client('dynamodb')

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']


def convertToJson(items):
    # TODO IMPLEMENT
    return items


def getAllItem():
    # get item
    response = dynamo_client.scan()
    items = response['Items']
    logging.info(f"{items=}")
    return convertToJson(items)


def handler(event, context):
    try:
        # get all item
        allItem = getAllItem()

    except Exception as err:
        # error
        logger.error('Function exception: %s', err)
        traceback.print_exc()
        logger.error('Failed to get all item')
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT,GET,DELETE',
            },
            'body': json.dumps({
                "message": "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost"
            }),
        }

    # suceeded
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT,GET,DELETE',
        },
        'body': json.dumps({
            "recipes": allItem
        }),
    }
