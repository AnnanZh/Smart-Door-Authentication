import json
import logging
import boto3
import time
from datetime import datetime
from datetime import timedelta
import random
from boto3 import client
from botocore.exceptions import ClientError
from botocore.retries import bucket

def lambda_handler(event, context):
    
    print(event)
    
    # Read Information
    body = event["body"]
    body = json.loads(body)
    
    visitor_name = body["message"]["firstname"]
    phone_number = body["message"]["phonenumber"]
    image_uuid = body["message"]["image_uuid"]
    
    #index face and get face id
    trimmed_name = visitor_name
    trimmed_name = trimmed_name.replace(" ", "")
    trimmed_name = trimmed_name.lower()
    faceid = add_face_to_collection(image_uuid, trimmed_name)

    # Save Visitor Information to DynamoDB
    dynamodb1 = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb1.Table('smartlockvisitors')
    putVisitorToDynamoDb(table, faceid, visitor_name, phone_number, image_uuid)

    # Save password to DynamoDB
    otp = generateOTP()
    time_out_value = 300
    save_password_to_db(otp, visitor_name, time_out_value)

    # send message with otp
    # sendSMS(phone, faceid, otp)
    send_otp_ses(otp, visitor_name)
    message = f"Thank you, {visitor_name} has been added to the database"
    return {
        'statusCode': 200,
        'body': message
    }

def add_face_to_collection(image_uuid, external_image_id):
    bucket = "hw3-visitor-photos"
    collection_id = "faces"
    client=boto3.client('rekognition')
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':f"{image_uuid}.jpg"}},
                                ExternalImageId=external_image_id,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
    print(f'Result for {external_image_id}')
    print('Faces indexed:')
    face_id = []
    for faceRecord in response['FaceRecords']:
        face_id.append(faceRecord['Face']['FaceId'])
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    return face_id[0]

#Checked
def putVisitorToDynamoDb(table, faceid, name, phone, photoid):
    table.put_item(
        Item = {
            'faceid': faceid,
            'name': name,
            'phone': phone,
            'photos': {
                'objectKey' : f"{photoid}.jpg",
                'bucket' : "hw3-visitor-photos",
                'createdTimestamp' : int(datetime.now().timestamp())
                }
        }
    )


def save_password_to_db(otp, visitor_name, time_out_value):
    table_name = 'passcodes'
    expired_time = int(datetime.now().timestamp())+ time_out_value
    dynamo = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamo.Table(table_name)
    table.put_item(
        Item = {
            'passwd' : str(otp),
            'expired_time' : expired_time
        })

def generateOTP():
    return random.randint(100000,999999)
    


def sendSMS(phone, faceid, otp):
    sns = boto3.client(
        'sns',
        region_name = 'us-east-1')
    message = "Hello, Welcome In! Your OTP is: " + otp
    print(message)
    try:
        response = sns.publish(
            PhoneNumber = phone,
            Message = message
            )
    except KeyError:
        print("error in sending sms")

def send_otp_ses(otp, visitor_name):
    message = f"Hello, Welcome In, {visitor_name}! Your OTP is: {otp} "
    sendSES(message)

def sendSES(message):
    ses = boto3.client('ses', region_name = 'us-east-1')
    CHARSET = "UTF-8"
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    "yx2304@nyu.edu",
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': message,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': message,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': message,
                },
            },
            Source = "az2345@nyu.edu",
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])