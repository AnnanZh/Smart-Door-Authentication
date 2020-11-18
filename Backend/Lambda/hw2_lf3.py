import json
import boto3
import logging
from datetime import datetime
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    body = event["body"]
    body = json.loads(body)
    
    otp = body["message"]["passwd"]
    # print(otp)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('passcodes')
    id = table.scan(
        FilterExpression = Key('passwd').eq(otp)
    )
    # print(id['Items'])
    if(id['Items']) == []:
        message = "invalid OTP"
    else:
        message = "Please Enter. Welcome!"
    
    # message = validateOTP(response, otp)
    
    return {
        'headers': {"Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Credentials": True
        },
        'statusCode': 200,
        'body': message
    }