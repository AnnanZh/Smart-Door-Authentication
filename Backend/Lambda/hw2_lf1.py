from email import message
import json
import base64
import boto3
from numpy.testing._private.parameterized import param
import cv2
import random
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

def generateOTP():
    return random.randint(100000,999999)

def send_otp_ses(otp, visitor_name):
    message = f"Hello, Welcome In, {visitor_name}! Your OTP is: {otp} "
    sendSES(message)

def send_unknowface_url(url):
    message = f"You have a new unknow visitor, {url}"
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

def form_wp1_url(image_uuid):
    wp1_url = "https://hw3-websites-owner.s3.amazonaws.com/WP1.html"
    wp1_url += "?photo_id="
    wp1_url += str(image_uuid)
    return wp1_url

def getKinesisAPIEndpoint():
    stream_arn = "arn:aws:kinesisvideo:us-east-1:455006891805:stream/IP_CAM/1604743854978"
    api_name = 'GET_MEDIA_FOR_FRAGMENT_LIST'
    client = boto3.client("kinesisvideo")
    response = client.get_data_endpoint(StreamARN=stream_arn, APIName = api_name)
    return response["DataEndpoint"]
    

def savePhotoToS3(fragmentNum):
    #get kinesis video access permission
    stream_name = "IP_CAM"
    bucket = 'hw3-test-photos'
    v_uuid = uuid.uuid1()
    movie_temp_path = f'/tmp/{v_uuid}.mkv'
    image_temp_path = f"/tmp/{v_uuid}.jpg"
    image_name = f'{v_uuid}.jpg'

    endpoint = getKinesisAPIEndpoint()
    client = boto3.client('kinesis-video-archived-media', endpoint_url = endpoint)
    response = client.get_media_for_fragment_list( StreamName=stream_name,Fragments=[fragmentNum])
    movie_stream = response["Payload"].read()
    f = open(movie_temp_path, 'wb')
    f.write(movie_stream)
    f.close()

    vidcap = cv2.VideoCapture(movie_temp_path)
    
    success, frame = vidcap.read()
    vidcap.release()
    if success:
        cv2.imwrite(image_temp_path, frame)
        s3_client = boto3.client('s3')
        s3_client.upload_file(image_temp_path, bucket, image_name, ExtraArgs={'ACL':'public-read'})
        print(f"image path: \n{image_temp_path}")
        print("upload success")
        return v_uuid
        
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
    
def getEventResult(event):
    for record in event["Records"]:
        #for each record, save one photo to s3
        payload=base64.b64decode(record["kinesis"]["data"])
        json_data = json.loads(payload.decode('utf-8'))

        stream_uuid = uuid.uuid1()
        print(f"stream uuid: {stream_uuid}")
        # print("Decoded payload: " + str(json_data))
        facesearch_response = json_data["FaceSearchResponse"]
        for face in facesearch_response:
            if face['MatchedFaces']:
                firstFace = face['MatchedFaces'][0]['Face']
                face_id = firstFace['FaceId']
                image_id = firstFace['ImageId']
                externeImageID = firstFace['ExternalImageId']
                print(externeImageID)
                print(f"stream {stream_uuid}")
                # fragmentNum = json_data['InputInformation']['KinesisVideo']['FragmentNumber']
                return (True, externeImageID, None)
            else:
                #get fragmentNum for later use
                fragmentNum = json_data['InputInformation']['KinesisVideo']['FragmentNumber']
                return (False, None, fragmentNum)


def lambda_handler(event, context):
    # TODO implement
    success, visitor_name, framentNum = getEventResult(event)
    if success:
        otp = generateOTP()
        save_password_to_db(otp, visitor_name, 300)
        send_otp_ses(otp, visitor_name)
    else:
        image_uuid = savePhotoToS3(framentNum)
        url = form_wp1_url(image_uuid)
        send_unknowface_url(url)
    return {
        'statusCode': 200,
        'body': json.dumps("Hello world")
    }
