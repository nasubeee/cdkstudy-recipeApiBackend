from asyncio.windows_events import NULL
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


def updateItem(id: str, new_title, new_making_time, new_serves, new_ingredients):
    # TODO IMPLEMENT
    pass


def handler(event, context):
    # Print received event
    logger.info(f"{event=}")
    try:
        # get item id from path parameters
        id = event['pathParameters']['id']
        # get item info from event
        item_data = json.loads(event['body'])
        new_title = item_data['title'] # TODO FIX IF NOT EXISTS
        new_making_time = item_data['making_time'] # TODO FIX IF NOT EXISTS
        new_serves = item_data['serves'] # TODO FIX IF NOT EXISTS
        new_ingredients = item_data['ingredients'] # TODO FIX IF NOT EXISTS
        new_cost = item_data['cost'] # TODO FIX IF NOT EXISTS
        # update item
        updateItem(
            id=id, new_title=new_title, new_making_time=new_making_time,
            new_serves=new_serves, new_ingredients=new_ingredients,
            new_cost=new_cost
        )

    except Exception as err:
        # error
        logger.error('Function exception: %s', err)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT,GET,DELETE',
            },
            'body': json.dumps({
                "message": "No Recipe found"
            }),
        }

    # suceeded
    logger.info(f"Item updated. {id=}")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT,GET,DELETE',
        },
        'body': json.dumps({
            "message": "Recipe successfully updated!",
            "recipe": [
                {
                    "id": id,
                    "title": new_title,
                    "making_time": new_making_time,
                    "serves": new_serves,
                    "ingredients": new_ingredients,
                    "cost": new_cost,
                }
            ]
        }),
    }
