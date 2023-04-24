# SumUp Take Home Test

The goal of this technical test is to showcase an end to end ELT pipeline from a data source to data warehouse using Python, SQL, and DBT and data models to answer business questions.

### Folder Structure
The whole repo is initialized as a DBT project. Some additional folders are added to the project structure:
- **sample_data**: Contains the raw data in CSV format.
- **scripts**: Contains the Python scripts used to extract and transform the data.

**analyses** folder contains the SQL queries used to answer the business questions defined in the task description.

I've used DBT cloud in order to make configuration with BigQuery connection easier.

## Envisioned Data Pipeline
The envisioned data pipeline will be an ELT pipeline that will extract raw data from the source csv files, load them into storage buckets, and then a data warehouse, and lastly use data models to transform the datasets. 
The data warehouse will be BigQuery, as I already have a personal GCP account. The raw data will be extracted from given CSV files, and loaded into the Cloud Storage buckets and BigQuery using Python, transformations will be done with DBT. The data warehouse will be modeled using DBT and will be used to answer business questions written in the task description.

The extracted raw data would be put into a cloud storage bucket (in this case Google Cloud Storage), where it would be stored as staging (bronze) data. The bronze data is the 1:1 representation of the raw data that is cleaned, but steps like common naming conventions and basic type configuraitons are applied. 
Afterwards, the data would be loaded into a cloud data warehouse (Google BigQuery) where it would be stored as a silver data. Silver data corresponds to data that is enriched (e.g. more advanced type castings are applied) and analytics friendly. The data would then be transformed using DBT and stored as a gold layer. The gold layer be would the aggregated business data, and serves a specific business use case.

In my solution implementation the data quality categories (raw, bronze, silver and gold) mentioned above are applied in structure. The whole pipeline can be containerized with Docker to make it easier to run and deploy, and can be orchestrated with Airflow to schedule the pipeline to run at specific times.

The extract and load steps of the pipeline are handled by separate Python scripts, as they are planned to run as individual tasks in Airflow.

### Architecture Diagram

The steps are as follows:
    - Read the three local CSV files with Python to gather bronze data  --> In an envoirement where more computation resources are avalible, PySpark can also be suitable tech choice for this and the next step due to its ability to process very large volumes of data in a distributed manner, thus enabling the pipeline to scale. Other features such as speed, ease of use are also important.
    - Write the extracted bronze data into Google Cloud Storage buckets.
    - Load data from Google Cloud Storage buckets into BigQuery under raw_dataset.
    - Create the staging tables with SQL via DBT to generate silver data.
    - Run the DBT models on staging tables to transform the data into the desired format, and have data model tables again as enriched (silver) data in the BigQuery.
    - Further transform and test the data with SQL via DBT.


## Datasets and Schemas
The dataset consists of 3 CSV files, each containing raw data about a different entity. The data types of the columns are assumptions based on common practises and past experiences. The entities are:
- **Stores**: Contains information about the stores, which are physical locations where their business happens.
    - **id (int, primary key)**: Unique identifier for the store.
    - **name (string)**: Name of the store.
    - **address (string)**: Address of the store.
    - **city (string)**: City where the store is located.
    - **country (string)**: Country where the store is located.
    - **created_at (datetime)**: Timestamp of when the store was created.
    - **typology (varchar)**: Business area/type of the store.
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
    - **status (varchar)**: Status of the transaction (accepted, cancelled, refused).
    - **card_number (string)**: Card number of the card that was used to make the transaction.
    - **cvv (varchar)**: CVV of the card that was used to make the transaction.
    - **created_at (datetime)**: Timestamp of when the transaction was created.
    - **happened_at (datetime)**: Timestamp of when the transaction happened.

    


Future improvements:
- The data pipeline can be containerized with Docker to make it easier to run and deploy, and can be orchestrated with Airflow to schedule the pipeline to run at specific times.
- Check for PII data and look into pseudonymization of the data due to GDPR regulations.
- Customer data deletion should be handled with a data retention and right to be forgotten policy.
- For the simplicity reasons the new data is appended to the existing tables. In a real world scenario, the transactions and stores production data should be partitioned by date, and the new data should be loaded into the correct partition.
