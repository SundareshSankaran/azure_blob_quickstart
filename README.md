# Azure Blob Storage Browser

<mark> (Initial Version - more details soon)</mark>

## Overview
This is an emergent application to help users browse and download the contents of an Azure storage account.
Why?  Many applications, but the main motivation is to provide a convenient means of accessing Azure Blob storage and data from other applications, an example being SAS.

# How to install

This [requirements.txt](./build/requirements.txt) file in the [build](./build/) directory provides a list of required Python packages (plus some optional conveniences) which you can either install in your Python environment or a virtual Python environment.

This [build.sh](./build/build.sh) shell script provides instructions and commands to create a virtual environment and install packages.

```bash
git clone https://github.com/SundareshSankaran/azure_blob_quickstart.git
cd build
./build.sh
```

# Options to run

**Prerequisite:** Check with your Azure Storage Account admin to ensure you have appropriate permissions to perform desired operations on an account.  Obtain an access key and save it in a .env file in your *local* repo folder.  Take care to protect your key.

```
AZURE_STORAGE_CONNECTION_STRING="<your key>"
```
With some modification, you can also use the passwordless auth mechanism.  Refer [here](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli&pivots=blob-storage-quickstart-scratch).

1. **Standalone Python Program:** Refer [block_quickstart.py](./blob_quickstart.py)

Here are snippets for the operations you can perform:

- List containers

```bash
python blob_quickstart.py list_containers
```

- List blobs in a container

```bash
python blob_quickstart.py list_blobs <container_name> 
```

- Search for a blob (based on a name pattern) in a container

```bash
python blob_quickstart.py search_blob <container_name> <search_term>
```

- Download a blob

```bash
python blob_quickstart.py download_blob <container_name> <blob_name> <download_path_on_client_machine>
```

- Upload a local file to a blob

```bash
python blob_quickstart.py upload_blob <container_name> <path_to_file_on_local_machine> <blob_name>
```

Or, optionally, if you omit the blob name, the local file name will be used instead.  

```bash
python blob_quickstart.py upload_blob <container_name> <path_to_file_on_local_machine> 
```

2. **Python Class**:  The [Python class defined here: blob_access_class.py](./blob_access_class.py) provides the same functionality as methods accessible from an instance of a BlobAccessClass. Refer this [example notebook](./tests/test_class.ipynb) for details on how to use.

3. **Streamlit app:**

```bash
# Ensure you activate the virtual environment
. build/azureblobtest/bin/activate

cd azure-blob-streamlit-app
streamlit run src/app.py

```

## Contact
- @SundareshSankaran ([email](mailto:sundaresh.sankaran@gmail.com))

## Version 
- Version 0.1.0 (see [Change Log](./CHANGELOG.md) for details)