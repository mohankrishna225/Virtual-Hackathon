import boto3
from botocore.exceptions import ClientError
import json
import os
import time
import uuid
import decimal

client = boto3.client('ses', region_name="us-east-1")
sender = "www.krishna225@gmail.com"
subject = "VirtualHackathon"
charset = 'UTF-8'

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')

def tamil(text):
    response = translate.translate_text(Text=text,SourceLanguageCode="auto",TargetLanguageCode="ta")
    print(response["TranslatedText"])
    return (response["TranslatedText"])


def hindi(text):
    response = translate.translate_text(Text=text,SourceLanguageCode="auto",TargetLanguageCode="hi")
    print(response["TranslatedText"])
    return (response["TranslatedText"])


def sendMail(event, context):
    print(event)

    try:
        data = event['body']
        content = 'Sender Email: ' + data['email'] + ',<br> FullName: ' + hindi(data['firstname']) + hindi(data['lastname']) + ',<br> Message Contents: ' + data['message']
        id = str(uuid.uuid1())
        saveToDynamoDB(data,id)
        saveTohindiDynamoDB(data,id)
        saveTotamilDynamoDB(data,id)
        toMail= str(data['email'])
        response = sendMailToUser(data, content,toMail)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:"),
        print(response['MessageId'])
    return "Email sent!"

def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all records from database
    result = table.scan()

    #return response
    return {
        "statusCode": 200,
        "body": result['Items']
    }



def saveToDynamoDB(data,id):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': id,
        'firstname': data['firstname'],
        'lastname': data['lastname'],
        'email': data['email'],
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return

def saveTohindiDynamoDB(data,id):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(os.environ['DYNAMODB_HINDI_TABLE'])
    item = {
        'id': id,
        'firstname': hindi(data['firstname']),
        'lastname': hindi(data['lastname']),
        'email': data['email'],
        'message': hindi(data['message']),
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return


def saveTotamilDynamoDB(data,id):
    timestamp = int(time.time() * 1000)
    # Insert details into DynamoDB Table
    table = dynamodb.Table(os.environ['DYNAMODB_TAMIL_TABLE'])
    item = {
        'id': id,
        'firstname': tamil(data['firstname']),
        'lastname': tamil(data['lastname']),
        'email': data['email'],
        'message': tamil(data['message']),
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return





def sendMailToUser(data, content,toMail):
    # Send Email using SES
    return client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                sender,
            ],
        },
        Message={
            'Subject': {
                'Charset': charset,
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': content
                }
            }
        }
    )
