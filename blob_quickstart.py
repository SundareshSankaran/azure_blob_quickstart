import sys

user_command = { "operation": sys.argv[1],
                "argument1": sys.argv[2] if len(sys.argv) > 2 else None,
                "argument2": sys.argv[3] if len(sys.argv) > 3 else None,
                "argument3": sys.argv[4] if len(sys.argv) > 4 else None
                }

print(f"User command-line arguments: {user_command}")

# Authenticate to the Azure Storage account using the connection string
# Ensure you have the AZURE_STORAGE_CONNECTION_STRING environment variable set
# You can set it in your environment or use a .env file with the dotenv package

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Import dotenv to load environment variables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Check if the environment variable is set
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
except Exception as e:
    print(f"Error loading environment variable: {e}")
    raise

# Authenticate to the Azure Storage account using the connection string
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
except Exception as e:
    print(f"Error creating BlobServiceClient: {e}")
    raise

print("Blob service client created successfully.")

# Function to list all containers in the storage account
def list_containers(blob_service_client):
    try:
        containers = blob_service_client.list_containers()
        for container in containers:
            print(f"Container: {container.name}")
        return containers
    except Exception as e:
        print(f"Error listing containers: {e}")
        raise

# Function to get a specific container client
def get_container(blob_service_client, container_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        return container_client
    except Exception as e:
        print(f"Error getting container client: {e}")
        raise

# Function to list blobs in a specific container
def list_blobs(container_client):
    try:
        blobs = container_client.list_blobs()
        for blob in blobs:
            print(f"Blob: {blob.name}")
        return blobs
    except Exception as e:
        print(f"Error listing blobs: {e}")
        raise

# Function to search and get a specific blob in a container
def search_blob(container_client, search_term):
    try:
        print(f"Searching for blobs matching: {search_term}")
        all_blobs = container_client.list_blobs()
        search_results = []
        for blob in all_blobs:
            if search_term in blob.name:
                search_results.append(blob)
        return search_results
    except Exception as e:
        print(f"Error getting blob client: {e}")
        raise

# Function to download a blob to a local file
def download_blob(container_client, blob_name, download_file_path):
    import os
    if os.path.isdir(download_file_path):
        print("Is a directory")
        download_file_path = os.path.join(download_file_path, blob_name)
    elif os.path.isfile(download_file_path):
        print("Is a file")
        print(f"folder for this is {os.path.dirname(download_file_path)}")
        download_file_path = os.path.join(os.path.dirname(download_file_path), os.path.dirname(blob_name), os.path.basename(download_file_path))
    else:
        root, ext = os.path.splitext(download_file_path)
        if not ext:
            download_file_path = os.path.join(download_file_path,os.path.basename(blob_name))
            root=root 
        download_file_path = os.path.join(os.getcwd(),download_file_path)
    print(f"download_file_path is {download_file_path}")
    try:
        if not os.path.exists(os.path.dirname(download_file_path)):
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
            print("Created directory:", os.path.dirname(download_file_path))
        blob_client = container_client.get_blob_client(blob_name)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f"Blob '{blob_name}' downloaded to '{download_file_path}' successfully.")
    except Exception as e:
        print(f"Error downloading blob: {e}")
        print(download_file_path)
        raise

# Function to upload a file to a blob in a container
def upload_blob(container_client, file_path, blob_name):
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"File '{file_path}' uploaded to blob '{blob_name}' successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise

if user_command["operation"] == "list_containers":
    print("Listing containers...")
    containers = list_containers(blob_service_client)
    print("Containers listed successfully.")
elif user_command["operation"] == "get_container":
    if user_command["argument1"]:
        print(f"Getting container: {user_command['argument1']}")
        container_name = user_command["argument1"]
        container_client = get_container(blob_service_client, container_name)
        print(f"Container '{container_name}' client created successfully.")
    else:
        print("Please provide a container name as an argument.")
elif user_command["operation"] == "list_blobs":
    if user_command["argument1"]:
        print(f"Listing blobs in container: {user_command['argument1']}")
        container_name = user_command["argument1"]
        container_client = get_container(blob_service_client, container_name)
        blobs = list_blobs(container_client)
        print("Blobs listed successfully.")
elif user_command["operation"] == "search_blob":
    if user_command["argument1"] and user_command["argument2"]:
        print(f"Searching for blobs containing '{user_command['argument2']}' in container: {user_command['argument1']}")
        container_name = user_command["argument1"]
        search_term = user_command["argument2"]
        container_client = get_container(blob_service_client, container_name)
        search_results = search_blob(container_client, search_term)
        print(f"Search completed successfully with {len(search_results)} results found.")
        for result in search_results:
            print(f" - {result.name}")
    else:
        print("Please provide a container name and a search term as arguments.")
elif user_command["operation"] == "download_blob":
    if user_command["argument3"] == None:
        user_command["argument3"] = os.getcwd() 
    if user_command["argument1"] and user_command["argument2"] and user_command["argument3"]:
        print(f"Downloading blob '{user_command['argument2']}' from container '{user_command['argument1']}' to '{user_command['argument3']}'")
        container_name = user_command["argument1"]
        blob_name = user_command["argument2"]
        download_file_path = user_command["argument3"]
        container_client = get_container(blob_service_client, container_name)
        download_blob(container_client, blob_name, download_file_path)
    else:
        print("Please provide a container name, blob name, and download file path as arguments.")
elif user_command["operation"] == "upload_blob":
    import os
    if not user_command["argument3"]:
        user_command["argument3"] = os.path.basename(user_command["argument2"])
    if not user_command["argument3"]:
        user_command["argument3"] = str(uuid.uuid4())
    if user_command["argument1"] and user_command["argument2"] and user_command["argument3"]:
        print(f"Uploading file '{user_command['argument2']}' to blob '{user_command['argument3']}' in container '{user_command['argument1']}'")
        file_path = user_command["argument2"]
        blob_name = user_command["argument3"]
        container_name = user_command["argument1"]
        container_client = get_container(blob_service_client, container_name)
        upload_blob(container_client, file_path, blob_name)
    else:
        print("Please provide a container name, file path and a blob name as arguments.")