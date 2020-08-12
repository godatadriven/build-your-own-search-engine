import json
import os

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from hotel_index import index

index_name = "hotels"
endpoint = os.environ["SEARCH_ENDPOINT"]
credential = AzureKeyCredential(os.environ["ACS_API_KEY"])


def initialize_index(endpoint:str, index:str, credential:str):
    """Create a search index

    Args:
        endpoint (str): url to azure cognitive search
        index (str): document index
        credential (str): azure cognitive search admin-key
    """
    client = SearchIndexClient(endpoint, credential)
    try:
        result = client.create_index(index)
    except HttpResponseError:
        pass


def upload_documents(endpoint:str, index_name:str, credential:str, documents:str):
    """Upload files that must be indexed

    Args:
        endpoint (str): url to azure cognitive search
        index_name (str): document index name
        credential (str): azure cognitive search admin-key
        documents (str): json file with documents according to the index schema
    """
    search_client = SearchClient(
        endpoint=endpoint, index_name=index_name, credential=credential
    )
    abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), documents)

    with open(abspath) as json_file:
        documents = json.load(json_file)

    result = search_client.upload_documents(documents=documents)


if __name__ == "__main__":
    initialize_index(endpoint, index, credential)
    upload_documents(endpoint, "hotels", credential, "hotel_documents.json")
