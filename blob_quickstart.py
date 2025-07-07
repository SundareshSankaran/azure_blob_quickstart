import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Import dotenv to load environment variables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

try:
    # Quickstart code goes here
    print("Azure Blob Storage Python quickstart sample")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    except Exception as e:
        print(f"Error creating BlobServiceClient: {e}")
        raise
    print("Blob service client created successfully.")

    # print(help(blob_service_client))
    print("Listing containers in the Blob service:")



        
    for a in blob_service_client.list_containers():
        print(a.name)   


    print("Containers listed successfully.")
    # print(help(blob_service_client))
    target_container = blob_service_client.get_container_client(container = "data-maker-synthetic-data")
    # List the blobs in the container
    blob_list = target_container.list_blobs()
    for blob in blob_list:
        if "golf" in blob.name:
            print("\t" + blob.name)

    target_blob_name = "golf-data/ALL_GOLF.parquet"
    print("\nDownloading blob to \n\t" )

    with open(file="/Users/sinsrn/current_projects/azure_blob_quickstart/target_file.parquet", mode="wb") as download_file:
        download_file.write(target_container.download_blob(target_blob_name).readall())



except Exception as ex:
    print('Exception:')
    print(ex)