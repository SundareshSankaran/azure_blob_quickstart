# Azure Blob Storage Browser

<mark> (In Progress)</mark>

## Overview
This is the beginning of an application to help users browse and download the contents of an Azure storage account.
Why?  Many applications, but specific to SAS, this provides convenience when reaching out to other applications which output to Azure Blob storage and such data is required by SAS.

# How to install

This [requirements.txt](./build/requirements.txt) file in the [build](./build/) directory provides a list of required packages (plus some conveniences) which you can either install in your Python environment, or through a virtual Python environment.

This [build.sh](./build/build.sh) shell script provides instructions on creating a virtual environment and installing the packages.

```bash
git clone https://github.com/SundareshSankaran/azure_blob_quickstart.git
cd build
./build.sh
```

# Options to run

**Prerequisite:** Check with your admin to ensure you have appropriate permissions to perform desired operations on this account.  Obtain an access key and save it in a .env file in your *local* repo folder.  Take care to protect your key.

```
AZURE_STORAGE_CONNECTION_STRING="<your key>"
```
With some modification, you can also use the passwordless auth mechanism.  Refer [here](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli&pivots=blob-storage-quickstart-scratch).

1. **Standalone Python Program:** Refer [block_quickstart.py](./blob_quickstart.py)
2. **Streamlit app:**

```bash
# Ensure you activate the virtual environment
. build/azureblobtest/bin/activate

cd azure-blob-streamlit-app
streamlit run src/app.py

```

## Contact
- @SundareshSankaran ([email](mailto:sundaresh.sankaran@gmail.com))
