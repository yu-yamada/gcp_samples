import base64, os, json
import urllib.request
channel = os.environ.get('SLACK_CHANNEL')
url = os.environ.get('WEBHOOK_URL')
def send_slack(payload):
   headers = {'Content-Type': 'application/json'}
   req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
   try:
       with urllib.request.urlopen(req) as res:
           body = res.read()
   except urllib.error.HTTPError as err:
       print(err.code)
   except urllib.error.URLError as err:
       print(err.reason)
def main_handler(event, context):
   pubsub_message = base64.b64decode(event['data']).decode('utf-8')
   print(pubsub_message)
   payload={
   'channel': channel,
   'username': 'hogehoge user',
   'attachments': [{
       'pretext': 'hogemoge.',
       'color': '#00F35A',
       'text': pubsub_message,
   }]
   }
   send_slack(json.dumps(payload).encode('utf-8'))
