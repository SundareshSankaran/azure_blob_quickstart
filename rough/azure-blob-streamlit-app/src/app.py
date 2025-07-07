import os
import streamlit as st
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure_blob_utils import list_containers, list_blobs_in_container, search_blobs_in_container, download_blob

# Load environment variables
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

def main():
    st.title("Azure Blob Storage Explorer")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Browse containers
    st.header("Browse Containers")
    containers = list_containers(blob_service_client)
    selected_container = st.selectbox("Select a container", containers)

    if selected_container:
        st.write(f"Selected container: {selected_container}")
        
        # Browse blobs in the selected container
        st.header("Browse Blobs")
        blobs = list_blobs_in_container(blob_service_client, selected_container)
        selected_blob = st.selectbox("Select a blob", blobs)

        if selected_blob:
            st.write(f"Selected blob: {selected_blob}")

            # Search for blobs
            st.header("Search for Blobs")
            search_pattern = st.text_input("Enter a wildcard pattern to search for blobs (e.g., 'golf*')")

            if search_pattern:
                search_results = search_blobs_in_container(blob_service_client, selected_container, search_pattern)
                st.write("Search Results:")
                for result in search_results:
                    st.write(result)
                selected_blob = st.selectbox("Select a blob", search_results, key=result[0])


            # Download selected blob
            if st.button("Download Blob"):
                download_blob(blob_service_client, selected_container, selected_blob)
                st.success(f"Blob '{selected_blob}' downloaded successfully.")

if __name__ == "__main__":
    main()