from google.cloud import bigquery
import base64, sys, os
def pubsub_to_bq(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    to_bigquery(os.environ['dataset'], os.environ['table'], os.environ['column'], pubsub_message)
def to_bigquery(dataset, table, column, document):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset)
    table_ref = dataset_ref.table(table)
    table = bigquery_client.get_table(table_ref)
    errors = bigquery_client.insert_rows(table, [{column:document}])
    if errors != [] :
        print(errors, file=sys.stderr)
