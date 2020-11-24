from django.http import HttpResponse
from django.http import JsonResponse
from azure.storage.blob import BlobServiceClient
#from pathlib import Path
import os
from io import BytesIO
import base64
import json 

LOCAL_BLOB_PATH = "reports"
def save_blob(file_name,file_content):
    # Get full path to the file
    #download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)
    download_file_path = file_name

    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

    with open(download_file_path, "wb") as file: 
      file.write(file_content)     
      

def index(request):
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=batchdatasciencedev;AccountKey=G6VcEwo2mFVPhBNIE0domk6Kwm5KyTW496t+dTLawwZYHVrflvegNI3TFL9u14OpBVUkJ6TBAf7yWMEW+KMC/g==;EndpointSuffix=core.windows.net'
    # blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    # DEST_FILE ='c\science\new\data.txt'
    #    # Instantiate a new ContainerClient
    # container_client = blob_service_client.get_container_client("batchtasksoutput3")
    #       # Create new Container in the service
    # container_client.create_container()
    #       # Instantiate a new BlobClient
    # blob_client = container_client.get_blob_client("myblockblob")
    # with open(DEST_FILE, "wb") as my_blob:
    #     download_stream = blob_client.download_blob()
    #     my_blob.write(download_stream.readall())


    blob_service_client =  BlobServiceClient.from_connection_string(connection_string)
    my_container = blob_service_client.get_container_client('batchtasksoutput')

    my_blobs = my_container.list_blobs()
    blob_url_dict = {}
    blob_url_dict_list={}
    for blob in my_blobs:
      print("blob.name")    
      bytes = my_container.get_blob_client(blob).download_blob().readall()      
    #   blob_url_dict[blob.name] = blob.name 
      encoded = base64.b64encode(bytes)
      #blob_url_dict[blob.name+'_Value'] = encoded.decode('ascii')
      blob_url_dict[blob.name] = encoded.decode('ascii')  
     
      print(json.dumps(blob_url_dict))    

    return JsonResponse(data={'blob_url':blob_url_dict})

    #return HttpResponse("Hello, world. You're at the polls index.")