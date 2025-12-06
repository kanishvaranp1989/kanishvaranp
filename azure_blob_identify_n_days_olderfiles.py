import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta, timezone
from send2trash import send2trash

#get connection string from azure storage account "ConnectionString" under "access keys" section
connection_string = "" 
container_name = '' #give container name
folder_prefix = "" #Folders available inside containers
file_prefix="giveany" #stores all listed files from blob to write in this file
local_folder_path="" #local path

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# threshold 
days_old = 60
cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)

print(f"Listing blobs older than {days_old} days:")

#my_dict={} # uncomment this if you are using dict section
key_to_add = "NA"
value_to_add = 1

#remove file with specific prefix
def remove_existing_file(file_prefix):
     if not file_prefix or len(file_prefix)==0:
         return False
     os.listdir(local_folder_path)
     for file in os.listdir(local_folder_path):
         if file.startswith(file_prefix+container_name):
             #if you use os.remove, it will permanently delete the file/ so using send2trash to move to recycle bin
             send2trash(os.path.join(local_folder_path, file))
             print(f"Removed existing file: {file}")
     return True

#write number of files in blob older than threshold to a file
def file_count_blob(container_client):
    for blob in container_client.list_blobs(name_starts_with=folder_prefix):
        if blob.last_modified < cutoff_date:        
            if "init.txt" not in blob.name:               
                with open(f"my_file_blob_{container_name}.txt", "a") as f:
                    print(f"{blob.name.rsplit('/', 1)[0]}\n")
                    f.write(f"{blob.name.rsplit('/', 1)[0]}\n")
                    f.close()
        #Use below code to number of files per blob folder and write as dictionary in file
                # print(f"Total files older than {days_old}")
                #print(f"{blob.last_modified < cutoff_date} :: {blob.name}")
                #key_to_add=blob.name.rsplit("/", 1)[0]
                #my_dict[key_to_add] = my_dict.get(key_to_add, 0) + value_to_add            
                #print(blob.name, "| Last Modified:", blob.last_modified,": ",key_to_add)
                # with open("my_file_blob.txt", "w") as f:
#              #f.write(blob.name.rsplit("/", 1)[0]+"\n")
#              for k,v in my_dict.items():
#                 print(f"{k} - {v}+\n")
#                 f.write(f"{k}-{v}+\n")
#              f.close()
            #print(my_dict)

print(remove_existing_file(file_prefix))
file_count_blob(container_client)
