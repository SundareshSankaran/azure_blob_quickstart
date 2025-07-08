import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client(connection_string):
    return BlobServiceClient.from_connection_string(connection_string)

def list_containers(blob_service_client):
    return [container.name for container in blob_service_client.list_containers()]

def list_blobs_in_container(blob_service_client, container_name):
    container_client = blob_service_client.get_container_client(container_name)
    return [blob.name for blob in container_client.list_blobs()]

def search_blobs_in_container(blob_service_client, container_name, search_pattern):
    container_client = blob_service_client.get_container_client(container_name)
    return [blob.name for blob in container_client.list_blobs() if search_pattern in blob.name]

def download_blob(blob_service_client, container_name, blob_name, download_file_path=os.getcwd()):
    container_client = blob_service_client.get_container_client(container_name)
    print(download_file_path)
    print(os.path.dirname(blob_name))
    if not os.path.exists(os.path.join(download_file_path, os.path.dirname(blob_name))):
        os.makedirs(os.path.join(download_file_path, os.path.dirname(blob_name)), exist_ok=True)
        print("Created directory:", os.path.join(download_file_path, os.path.dirname(blob_name)))
    print(download_file_path)
    with open(os.path.join(download_file_path, blob_name), mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob_name).readall())