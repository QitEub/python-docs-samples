from google.cloud import bigquery
import pytest
import google.cloud.exceptions
import uuid

client = bigquery.Client()
dataset_UUID = str(uuid.uuid4()).split("-")[0]


@pytest.fixture(scope="module")
def dataset():
  
    dataset_id = format(client.project)+".sample_dataset"+dataset_UUID
    dataset = bigquery.Dataset(dataset_id)
    
    try:
        dataset = client.get_dataset(dataset_id)
    except google.cloud.exceptions.NotFound:
        dataset = client.create_dataset(dataset) 

    yield dataset

    client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)

@pytest.fixture(scope="module")
def table():

    table_id = client.project+".sample_dataset"+dataset_UUID+".average_weather"

    schema = [
        bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
        bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
        bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE")
    ]

    table = bigquery.Table(table_id, schema=schema)

    try:
        table = client.get_table(table_id)  # Make an API request.
    except google.cloud.exceptions.NotFound:
        table = client.create_table(table)

    yield table_id

    client.delete_table(table_id, not_found_ok=True)

def test_dataset_creation(dataset, table):

    table = client.get_table(table)
    schema = table.schema
    dataset = dataset.dataset_id

    schemaTest = schema = [
        bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
        bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
        bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE")
    ]  
    assert table.table_id == "average_weather"
    assert schema == schemaTest
    assert dataset == "sample_dataset"+dataset_UUID
   