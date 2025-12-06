from azure.storage.blob import BlobServiceClient

connection_string = "" # get connection from Azure storage account "Access key" -->"Connection string"
container_name = "" # containername
folder_prefix = "" #blob folder prefix
LOCAL_FILE_PATH = "" # local folder
filename = "" #if file name is filename.txt, can give "file" or "name" or ".txt"
blob_name=''
search_string=""
     

#grep file from blob
def grep_file(search_string,blob_name,container_name):
    try:
        # Get a BlobClient for the specific blob
        print(f"Running grep on blob: {blob_name} for search string: {search_string}")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        # Download the blob content as a string (or stream for very large files)
        # This reads the content directly into memory
        blob_content = blob_client.download_blob().readall().decode('utf-8')
        # Now, you can perform your "grep" operation on blob_content
        search_term = search_string
        found_lines = []
        for line in blob_content.splitlines():
            if search_term in line:
                found_lines.append(line)
                print(line)
        files=[]
        if found_lines:
            print(f"Found '{search_term}' in the following lines:")
            for line in found_lines:    
                files.append(f"{blob_name}::{line}")
        return files
    except Exception as ex:
        print(f"Error: {ex}")

# pass is_grep_string True to grep string in file
def file_lookup(file_name,container_name,folder_prefix,is_grep_string=False,search_string=""):
    if is_grep_string and len(search_string)==0:
        return ["Search string cannot be empty when grep option is selected."]
    if len(file_name)==0 or len(container_name)==0 or len(folder_prefix)==0:
        return ["File name pattern and Folder prefix cannot be empty."] 
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)   
        grepped_files=[]
        listed_files=[]
        count=0
        for blob in container_client.list_blobs(name_starts_with=folder_prefix):
            if file_name in blob.name and 'init.txt' not in blob.name:
                print(f"Matched blob: {blob.name}")
                count+=1
                if count>=1000:
                    break  #limit to first 1000 matches to avoid long processing times            
                if is_grep_string==True and not len(search_string)==0:
                   grep_files= grep_file(search_string,blob.name,container_name)
                   grepped_files.extend(grep_files)
                   grepped_files=list(set(grepped_files))
                else:
                     listed_files.append(blob.name)
                     listed_files=list(set(listed_files))                
        #print(f"Total files found: {count}::{is_grep_string}:::{(grepped_files)}:::{listed_files}")
        if is_grep_string:
            return grepped_files if len(grepped_files)>0 else ["No files found matching the criteria."]
        else:
            return listed_files if len(listed_files)>0 else ["No files found matching the criteria."]
        return   ["No files found matching the criteria."]
        
    except Exception as e:
        print("Error:", e)
        return ["Something went wrong. Please try again later."]

def file_download(file_name,container_name,folder_prefix):
    if not file_name or len(file_name) == 0:
        print("Invalid file name provided.")
        return False
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)        
        file_found = False
        print(f"Running download function for {file_name}...")  # Added space for readability

        for blob in container_client.list_blobs(name_starts_with=folder_prefix):
            if file_name in blob.name:
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
                with open(LOCAL_FILE_PATH + blob.name.split("/")[-1], "wb") as download_file:
                    download_stream = blob_client.download_blob()
                    download_file.write(download_stream.readall())
                file_found = True
                print(f"Downloaded: {blob.name}")  # Indicate successful download
                break  # Exit loop after downloading the file
        if not file_found:
            print(f"File '{file_name}' not found in the blob storage.")
        return file_found
    except Exception as e:
        print("Error:", e)
        return False


#Call the function and print the result
#print(file_lookup(filename,container_name,folder_prefix,True))
#print("File found completed successfully.")
