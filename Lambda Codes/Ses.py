import json
import boto3
import os
region_name = 'us-east-1'
def sendEmail(event, context):
    data = event['body']
    name = data ['name']    
    source = data['source']    
    subject = data['subject']
    message = data['message']    
    destination = data['destination']
    _message = "Message from: " + name + "\nEmail: " + source + "\nMessage content: " + message    
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': _message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
)
    return _message + str(region_name)                
    