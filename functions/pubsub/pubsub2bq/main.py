from google.cloud import bigquery
import base64, sys, os
import logging
import google.cloud.logging
client = google.cloud.logging.Client(project=os.environ['project_id'])
handler = client.get_default_handler()
cloud_logger = logging.getLogger('cloudLogger')
cloud_logger.setLevel(logging.INFO)  # defaults to WARN
cloud_logger.addHandler(handler)
def pubsub_to_bq(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    to_bigquery(os.environ['dataset'], os.environ['table'], os.environ['column'], pubsub_message)
def to_bigquery(dataset, table, column, document):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset)
    table_ref = dataset_ref.table(table)
    table = bigquery_client.get_table(table_ref)
    try:
        ret = bigquery_client.insert_rows(table, [{column:document}])
        print(ret)
        if  ret != [] :
            cloud_logger.error(ret)
            print(ret)
            sys.exit(1)
    except Exception as e:
        cloud_logger.error(e)
        print(ret)
        sys.exit(1)
