from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client(project="dbt-test-project-384521")

def setup_stores_table():
    """
    This function sets the load job configuration for the stores table and loads the data from the GCS bucket to the BigQuery table
    """
    # table_id to the ID of the table to create. Dataset is created manually in GCP
    table_id = "dbt-test-project-384521.raw_datasets.stores_source"
    uri = "gs://sumup_test_bucket/storesFile.csv"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("address", "STRING"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("country", "STRING"),
            bigquery.SchemaField("created_at", "STRING"),
            bigquery.SchemaField("typology", "STRING"),
            bigquery.SchemaField("customer_id", "INTEGER"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_TRUNCATE",
    )
    load_to_bq(uri, table_id, job_config)

def setup_devices_table():
    """
    This function sets the load job configuration for the devices table and loads the data from the GCS bucket to the BigQuery table
    """
    # table_id to the ID of the table to create. Dataset is created manually in GCP
    table_id = "dbt-test-project-384521.raw_datasets.devices_source"
    uri = "gs://sumup_test_bucket/devicesFile.csv"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("type", "INTEGER"),
            bigquery.SchemaField("store_id", "INTEGER"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_TRUNCATE",
    )
    load_to_bq(uri, table_id, job_config)

def setup_transactions_table():
    """
    This function sets the load job configuration for the transactions table and loads the data from the GCS bucket to the BigQuery table
    """
    # table_id to the ID of the table to create. Dataset is created manually in GCP
    table_id = "dbt-test-project-384521.raw_datasets.transactions_source"
    uri = "gs://sumup_test_bucket/transactionsFile.csv"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("device_id", "INTEGER"),
            bigquery.SchemaField("product_name", "STRING"),
            bigquery.SchemaField("product_sku", "STRING"),
            bigquery.SchemaField("product_name_copy", "STRING"),
            bigquery.SchemaField("amount", "FLOAT"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("card_number", "STRING"),
            bigquery.SchemaField("cvv", "STRING"),
            bigquery.SchemaField("created_at", "STRING"),
            bigquery.SchemaField("happened_at", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_TRUNCATE",
    )
    load_to_bq(uri, table_id, job_config)



def load_to_bq(uri, table_id, job_config):
    """
    This function loads the data from the GCS bucket to the BigQuery table
    """
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

# Call the functions to run data load
setup_stores_table()
setup_devices_table()
setup_transactions_table()