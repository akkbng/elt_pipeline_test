from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

#this script is used to upload the sample data to a GCP bucket, which will be serve as silver data in the pipeline, where we have a table structure and columns type set for the datafiles.

if __name__ == "__main__":
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('storage', 'v1', credentials=credentials)

    storesFile = "../sample_data/store_-_store.csv.csv"
    devicesFile = "../sample_data/device_-_device.csv.csv"
    transactionsFile = "../sample_data/transaction_-_transaction.csv.csv"

    fileList = [storesFile, devicesFile, transactionsFile]
    fileNames = ["storesFile.csv", "devicesFile.csv", "transactionsFile.csv"]

    bucket = "sumup_test_bucket" #created manually in GCP, with 2 years date retention policy

    for i in range(len(fileList)):
        req = service.objects().insert(bucket=bucket, name=fileNames[i], media_body=fileList[i])
        req.execute()
    
    print("Files uploaded to GCP bucket")

