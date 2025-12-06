from azure.storage.blob import BlobServiceClient

connection_string = "" # "Connection string" from "Access key" section in Storage account
container_name = "" #blob containername
folder_prefix = "" #blob folder prefix
LOCAL_FILE_PATH="" # local folder where file to be downloaded

def file_download(file_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        # list blobs
        file_found=False
        print(f"running download function{file_name}")
        for blob in container_client.list_blobs(name_starts_with=folder_prefix):
            if file_name in blob.name:
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
                with open(LOCAL_FILE_PATH+blob.name.split("/")[-1], "wb") as download_file: #write binary while download
                    download_stream = blob_client.download_blob()
                    download_file.write(download_stream.readall())
                file_found=True
        return file_found
    except Exception as e:
        print("Error:", e)
        return False
