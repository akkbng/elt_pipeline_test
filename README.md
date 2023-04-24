# ELT Pipeline Take Home Test

The goal of this test is to showcase an end to end ELT pipeline from a data source to data warehouse using Python, SQL, and DBT and data models to answer business questions.

### Folder Structure
- **scripts**: Contains the Python scripts used to extract and load the data. 
    - **extract_to_gs.py**: Reads the CSV files and writes them into Google Cloud Storage buckets.
    - **load_to_bq.py**: Loads the data from Google Cloud Storage buckets into BigQuery.
- **sumup**: Contains the standard DBT project setup.
    - **analyses** folder  the contains the SQL queries used to answer the business questions defined in the task description. As these questions were more like ad-hoc analysis, I have written the queries as analyses instead of models.
- **airflow**: Contains the DAG file that orchestrates the pipeline with airflow.
    - **docker-compose.yml**: Contains the Docker Compose file that is used to run the pipeline.


## Envisioned Data Pipeline
The envisioned data pipeline will be an ELT pipeline that will extract raw data from the source csv files, load them into storage buckets and a data warehouse, and lastly use data models to transform the datasets. 
The data warehouse will be BigQuery, as I already have a personal GCP account. The raw data will be extracted from given CSV files, and loaded into the Cloud Storage buckets and BigQuery using Python, transformations will be done with DBT. The data warehouse will be modeled using DBT and will be used to answer business questions written in the task description.

The extracted raw data would be put into a cloud storage bucket (in this case Google Cloud Storage), where it would be stored as "bronze" data. The bronze data is the 1:1 representation of the raw data where steps like common naming conventions and basic type configurations are applied. 
Afterwards, the data would be loaded into a cloud data warehouse (Google BigQuery) where it would be stored as a staging (silver) data. Silver data corresponds to data that is enriched (e.g. more advanced type castings are applied) and analytics friendly. The data would then be transformed using DBT and stored as a gold layer. The gold layer be would the aggregated business data, and serves a specific business use case. In my solution the data quality categories (raw, bronze, silver and gold) mentioned above are applied in structure.

The extract and load steps of the pipeline are handled by separate Python scripts, as they are planned to run as individual tasks in Airflow.

### Architecture Diagram

![alt text](https://github.com/akkbng/elt_pipeline_test/blob/main/pipeline.png)


The steps are as follows:
    - Read the three local CSV files with Python to gather raw data 
    - Write the extracted bronze data into Google Cloud Storage buckets.
    - Load data from Google Cloud Storage buckets into BigQuery under raw_dataset.
    - Test and create the staging tables with SQL via DBT to generate silver data.
    - Run the DBT models on staging tables to transform the data into the desired format, and have data model tables again as gold data in the BigQuery. In this case, only the 'transactions' table is planned as gold data, as for most of the queries the staging tables were enough.
    - Further transform and test the data via DBT.


## Datasets and Schemas
The dataset consists of 3 CSV files, each containing raw data about a different entity. The data types of the columns are assumptions based on common practises and past experiences. The entities are:
- **Stores**: Contains information about the stores, which are physical locations where their business happens.
    - **id (int, primary key)**: Unique identifier for the store.
    - **name (string)**: Name of the store.
    - **address (string)**: Address of the store.
    - **city (string)**: City where the store is located.
    - **country (string)**: Country where the store is located.
    - **created_at (datetime)**: Timestamp of when the store was created.
    - **typology (string)**: Business area/type of the store.
    - **customer_id (int)**: Unique identifier for the customer that owns the store.
- **Devices**: Contains information about the devices that are used to make transactions at the stores.
    - **id (int, primary key)**: Unique identifier for the device.
    - **type (int)**: Type of the device (1 to 5).
    - **store_id (int, foreign key to stores.id)**: Unique identifier of the store that the device is located at.
- **Transactions**: Contains information about the transactions that happen at the stores.
    - **id (int, primary key)**: Unique identifier for the transaction.
    - **device_id (int, foreign key to devices.id)**: Unique identifier of the device that the transaction was made on.
    - **product_name (string)**: Name of the product that was bought.
    - **product_sku (varchar)**: SKU of the product that was bought. Unique identifier for the product.
    - **product_name (string)**: Name of the product that was bought.
    - **amount (float)**: Amount of the transaction in euro.
    - **status (string)**: Status of the transaction (accepted, cancelled, refused).
    - **card_number (string)**: Card number of the card that was used to make the transaction.
    - **cvv (string)**: CVV of the card that was used to make the transaction.
    - **created_at (datetime)**: Timestamp of when the transaction was created.
    - **happened_at (datetime)**: Timestamp of when the transaction happened.

    
## Future improvements:
- The data pipeline can be containerized with Docker to make it easier to run and deploy, and can be orchestrated with Airflow to schedule the pipeline to run at specific times.
- Check for PII data and look into pseudonymization of the data due to GDPR regulations.
- Customer data deletion should be handled with a data retention and right to be forgotten policy.
- For the simplicity reasons the new data is overwritten to the existing tables in the pipeline. In a real world scenario, the transactions and stores production data should be partitioned by date, and the new data should be loaded into the correct partition.
- CI/CD pipeline should be implemented to automate the testing and deployment of the pipeline.
