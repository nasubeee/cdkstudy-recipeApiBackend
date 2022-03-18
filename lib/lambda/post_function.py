import boto3
import logging
import datetime
import json
import os
import traceback

# Create logger
logger = logging.getLogger()
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# Create dynamodb client
dynamo_client = boto3.client('dynamodb')

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']


def createNewItem(title: str, making_time: str, serves: str,
                  ingredients: str, cost: str):
    # set id
    id = 0  # TODO FIX
    # set create date and update date
    created_datetime = datetime.datetime.now()
    created_at = created_datetime.strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at
    # put item
    response = dynamo_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "id": {"S": id},
            "title": {"S": title},
            "making_time": {"S": making_time},
            "serves": {"S": serves},
            "ingredients": {"S": ingredients},
            "cost": {"S": cost},
            "created_at": {"S": created_at},
            "updated_at": {"S": updated_at},
        },
        ConditionExpression='attribute_not_exists(id)'
    )
    logging.debug(f"{response=}")
    return response


def handler(event, context):
    # Print received event
    logger.debug(f"{event=}")
    try:
        # get item info from event
        item_data = json.loads(event['body'])
        logger.debug(f"{item_data=}")
        title = item_data['title']
        making_time = item_data['making_time']
        serves = item_data['serves']
        ingredients = item_data['ingredients']
        cost = item_data['cost']
        # create new item to the table
        created_item = createNewItem(title=title, making_time=making_time,
                                     serves=serves, ingredients=ingredients,
                                     cost=cost)

    except Exception as err:
        # error
        logger.error('Function exception: %s', err)
        traceback.print_exc()
        logger.error('Failed to create new item')
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
    logger.debug(f"New item created. {created_item=}")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT,GET,DELETE',
        },
        'body': json.dumps({
            "message": "Recipe successfully created!",
            "recipe": [
                {
                    "id": created_item['id'],
                    "title": created_item['title'],
                    "making_time": created_item['making_time'],
                    "serves": created_item['serves'],
                    "ingredients": created_item['ingredients'],
                    "cost": created_item['cost'],
                    "created_at": created_item['created_at'],
                    "updated_at": created_item['updated_at']
                }
            ]
        }),
    }
