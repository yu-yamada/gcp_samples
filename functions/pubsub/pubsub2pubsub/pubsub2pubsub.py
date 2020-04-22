import base64
from google.cloud import pubsub_v1
import json
import os

def hello_pubsub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    
    publisher = pubsub_v1.PublisherClient()
     
    topic_path = publisher.topic_path(os.environ.get('PROJECT_ID'), os.environ.get('TOPIC_NAME'))
    print(topic_path)
    
    message_json = json.dumps({
        'data': {'message': pubsub_message},
    })
    message_bytes = message_json.encode('utf-8')

    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Message published.'
    except Exception as e:
        print(e)
        return (e, 500)
