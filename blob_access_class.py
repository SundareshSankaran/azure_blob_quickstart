class BlobAccessClass:
    """
    This class provides methods to interact with Azure Blob Storage.
    It allows listing containers, getting a specific container client,
    listing blobs in a container, searching for blobs, downloading blobs,
    and uploading files to blobs.
    """

    def __init__(self, blob_service_client= None, container_list=[], container_client=None):
        """
        Initialize the BlobAccessClass with a BlobServiceClient.
        If no client is provided, it will create one using the connection string.
        """

        # Authentication steps to obtain a Blob Service Client, which can then be used for above operations.

        import os
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
        from dotenv import load_dotenv
        # Load environment variables
        load_dotenv()

        if blob_service_client is None:
            try:
                # Authenticate to the Azure Storage account using the connection string
                # Ensure you have the AZURE_STORAGE_CONNECTION_STRING environment variable set
                # You can set it in your environment or use a .env file with the dotenv package
                # Check if the environment variable is set
                connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
                if not connect_str:
                    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
                self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                print("Blob service client created successfully.")
            except Exception as e:
                print(f"Error creating BlobServiceClient: {e}")
                raise
            if container_list == []:
                self.list_containers()
            else:
                self.container_list = container_list
        else:
            self.blob_service_client = blob_service_client
            self.list_containers()
        self.container_client = container_client if container_client else None
        self.blobs = []

    # Method to list all containers in the storage account
    def list_containers(self):
        """
        List all containers in the storage account.
        Populates container_list with a list of container names.
        """
        try:
            containers = self.blob_service_client.list_containers()
            self.container_list = []
            for container in containers:
                self.container_list.append(container.name)
        except Exception as e:
            print(f"Error listing containers: {e}")
            raise
        for container in self.container_list:
            print(f"Container: {container}")

    # Method to get a specific container client
    def get_container(self, container_name):
        """
        Get a client for a specific container.
        Returns a ContainerClient object pointing to the specified container.
        """
        if not container_name:
            raise ValueError("Container name must be provided.")
        elif container_name not in self.container_list:
            raise ValueError(f"Container '{container_name}' does not exist in the storage account.")
        else:
            try:
                self.container_client = self.blob_service_client.get_container_client(container_name)
            except Exception as e:
                print(f"Error getting container client: {e}")
                raise


    # Method to list blobs in a specific container
    def list_blobs(self, blobs=None):
        """
        List all blobs in the specified container.
        If blobs is provided, it will be used to populate the blobs attribute.
        Prints a list of blob names in the container.
        """
        self.blobs = blobs if blobs else []
        try:
            blobs = self.container_client.list_blobs()
            for blob in blobs:
                print(f"Blob: {blob.name}")
                self.blobs.append(blob.name)
        except Exception as e:
            print(f"Error listing blobs: {e}")
            raise

    # Method to search and get a specific blob in a container
    def search_blob(self, search_term):
        """
        Search for blobs in the container that match the search term.
        Returns a list of blobs that match the search term.
        """
        try:
            print(f"Searching for blobs matching: {search_term}")
            all_blobs = self.container_client.list_blobs()
            self.search_results = []
            for blob in all_blobs:
                if search_term in blob.name:
                    self.search_results.append(blob.name)
            return self.search_results
        except Exception as e:
            print(f"Error getting blob client: {e}")
            raise

    # Method to download a blob to a local file
    def download_blob(self, blob_name, download_file_path):
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
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print(f"Blob '{blob_name}' downloaded to '{download_file_path}' successfully.")
        except Exception as e:
            print(f"Error downloading blob: {e}")
            print(download_file_path)
            raise

    # Method to upload a file to a blob in a container
    def upload_blob(self, file_path, blob_name):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"File '{file_path}' uploaded to blob '{blob_name}' successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise
