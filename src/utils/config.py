import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    ENDPOINT = os.getenv("ENDPOINT_BLOB") 
    KEY = os.getenv("SUBSCRIPTION_KEY_BLOB")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("CONTAINER_NAME")

    ENDPOINT_DOC = os.getenv("ENDPOINT_DOC") 
    KEY_DOC = os.getenv("SUBSCRIPTION_KEY_DOC")
