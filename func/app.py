import base64
import io
import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')
S3 = boto3.client('s3')

COLLECTION_ID = os.getenv("COLLECTION_ID")
TABLE_NAME = os.getenv("TABLE_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def search_faces_by_image(decoded_image):
    try:
        response = rekognition.search_faces_by_image(
            Image={'Bytes': decoded_image}, CollectionId=COLLECTION_ID)
    except Exception as e:
        print(e)
        return None
    else:
        return response


def index_faces(decoded_image):
    try:
        response = rekognition.index_faces(
            Image={'Bytes': decoded_image}, CollectionId=COLLECTION_ID)
    except Exception as e:
        print(e)
        return []
    else:
        return response['FaceRecords']


def increment_index_count(faceId):
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'RekognitionId': faceId}, )
    item = response['Item'] if 'Item' in response else {}
    if "Count" not in item: item["Count"] = 0
    item["Count"] += 1
    table.put_item(
        TableName=TABLE_NAME,
        Item={
            'RekognitionId': faceId,
            "Count": item["Count"]
        })
    return item["Count"]


def store_image(name, decoded_image):
    byteobj = io.BytesIO(decoded_image)
    S3.upload_fileobj(byteobj, BUCKET_NAME, name)


def handler(event, context):
    message = json.loads(event["body"])
    decoded_image = base64.decodebytes(message["image"].encode())
    search_result = search_faces_by_image(decoded_image)
    if search_result is None:
        print("no face found")
    elif (search_result['SearchedFaceConfidence'] >= 90
          and len(search_result['FaceMatches']) > 0):
        face_id = search_result['FaceMatches'][0]['Face']['FaceId']
        count = increment_index_count(face_id)
        print(f"record found: {face_id}, ({count})")
    else:
        face_records = index_faces(decoded_image)
        for face in face_records:
            increment_index_count(face["Face"]["FaceId"])
            print("new face:", face["Face"]["FaceId"])
            store_image(face["Face"]['FaceId'] + ".png", decoded_image)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(message)
    }
