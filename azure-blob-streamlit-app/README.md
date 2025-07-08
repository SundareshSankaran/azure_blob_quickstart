# Azure Blob Streamlit App

This project is a Streamlit application that allows users to interact with Azure Blob Storage. Users can browse containers, view blobs within those containers, search for specific blobs using wildcard patterns, and download selected blobs.

## Project Structure

```
azure-blob-streamlit-app
├── src
│   ├── app.py                # Main entry point of the Streamlit application
│   └── azure_blob_utils.py   # Utility functions for Azure Blob Storage interactions
├── requirements.txt          # List of dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd azure-blob-streamlit-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Azure Storage credentials:**
   Ensure you have your Azure Storage connection string set in your environment variables. You can do this by creating a `.env` file in the root directory with the following content:
   ```
   AZURE_STORAGE_CONNECTION_STRING=<your_connection_string>
   ```

## Usage

To run the Streamlit application, execute the following command in your terminal:

```bash
streamlit run src/app.py
```

Once the application is running, you can access it in your web browser at `http://localhost:8501`.

## Features

- **Browse Containers:** View all containers in your Azure Blob Storage account.
- **Browse Blobs:** List all blobs within a selected container.
- **Search Blobs:** Use wildcard patterns to search for specific blobs.
- **Download Blobs:** Download a selected blob to your local machine.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.