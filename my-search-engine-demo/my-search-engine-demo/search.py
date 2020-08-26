# Setup a search service on an azure blob container
import requests
import os
from azure.core.exceptions import HttpResponseError
import logging
from time import sleep
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Setup a search service on an azure blob container
import requests
import os
from azure.core.exceptions import HttpResponseError
import logging
from time import sleep
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

class SearchService:
    """Index Azure Blob with Azure Cognitive Search
    """
    def __init__(self):
        """Initialize required configurations
        Service name: name of search service
        API key: secret of search service
        API version: version of search API
        """
        self.url = os.environ["SEARCH_ENDPOINT"]
        self.headers = {
            "Content-Type": "application/json",
            "api-key": os.environ['ACS_API_KEY'],
        }
        self.api_version = "api-version=2020-06-30"
        self.connection_string = os.environ['PLAYGROUND_CONN_STR']
        self.container_name = "covid-news"
        self.index_name = "covid-19-index"
        self.indexer_name = "covid-19-indexer"
        self.data_source_name = "covid-19-data-source"

    def create_data_source(self):
        """Setup the blob
        connectionString: connection string from storage account
        container: name of container in storage account
        """

        data_source_schema = {
            "name": self.data_source_name,
            "type": "azureblob",
            "credentials": {"connectionString": self.connection_string},
            "container": {"name": self.container_name},
        }

        data_source_url = (
            self.url
            + "datasources?"
            + self.api_version
        )

        try:
            response = requests.post(
                data_source_url, headers=self.headers, json=data_source_schema
            )
            if response.status_code == 201:
                LOGGER.info("SUCCESSFULL POST request to %s. Returned status code %s",data_source_url, response.status_code)
            else:
                LOGGER.info("UNSUCCESSFULL POST request to %s. Returned status code %s",data_source_url, response.status_code)
                LOGGER.info("Body: %s", response.json())
        except HttpResponseError as e:
            print("Data source already exists: %s", e)

    def create_index(self):
        """Create a schema for how the documents in the blob should be indexed
        """
        index_schema = {
            "name": "covid-19-index",
            "fields": [
                {
                    "name": "id",
                    "type": "Edm.String",
                    "key": "true",
                    "searchable": "false",
                },
                {
                    "name": "timestamp",
                    "type": "Edm.String",
                    "searchable": "false",
                    "filterable": "false",
                    "sortable": "false",
                    "facetable": "false",
                },
                {
                    "name": "source",
                    "type": "Edm.String",
                    "searchable": "false",
                    "filterable": "false",
                    "sortable": "false",
                    "facetable": "false",
                },
                {
                    "name": "title",
                    "type": "Edm.String",
                    "searchable": "true",
                    "filterable": "false",
                    "sortable": "false",
                    "facetable": "false",
                },
                {
                    "name": "body",
                    "type": "Edm.String",
                    "searchable": "true",
                    "filterable": "false",
                    "sortable": "false",
                    "facetable": "false",
                },
            ],
        }
        index_url = (
            self.url
            + "indexes?"
            + self.api_version
        )

        try:
            response = requests.post(index_url, headers=self.headers, json=index_schema)
            if response.status_code == 201:
                LOGGER.info("SUCCESSFULL POST request to %s. Returned status code %s",index_url, response.status_code)
            else:
                LOGGER.info("UNSUCCESSFULL POST request to %s. Returned status code %s",index_url, response.status_code)
                LOGGER.info("Body: %s", response.json())

        except HttpResponseError as e:
            print("Index already exists: %s", e)

    def create_indexer(self):
        """Create an indexer that will index the files in the Blob
        """
        indexer_schema = {
            "name": self.indexer_name,
            "dataSourceName": self.data_source_name,
            "targetIndexName": self.index_name,
            "parameters": {
                "configuration": {
                    "parsingMode": "jsonLines",
                    "dataToExtract": "contentAndMetadata",
                }
            },
        }
        indexer_url = (
            self.url
            + "indexers?"
            + self.api_version
        )

        try:
            response = requests.post(indexer_url, headers=self.headers, json=indexer_schema)
            if response.status_code == 201:
                LOGGER.info("SUCCESSFULL POST request to %s. Returned status code %s",indexer_url, response.status_code)
            else:
                LOGGER.info("UNSUCCESSFULL POST request to %s. Returned status code %s",indexer_url, response.status_code)
                LOGGER.info("Body: %s", response.json())
        except HttpResponseError as e:
            print("Indexer already exists: %s", e)

    def run_indexer(self):
        """Run the indexer to index the files in the blob
        """
        run_indexer_url = (
            self.url
            + f"indexers/{self.indexer_name}/run?"
            + self.api_version
        )
        response = requests.post(run_indexer_url, headers=self.headers)
        if response.status_code == 202:
            LOGGER.info("SUCCESSFULL POST request to %s. Returned status code %s",run_indexer_url, response.status_code)
            LOGGER.info("Checking indexer status...")
            self.check_indexer_status()
        else:
            LOGGER.info("UNSUCCESSFULL POST request to %s. Returned status code %s",run_indexer_url, response.status_code)

    def setup_search_service(self):
        """Setup the search service:
        Create the data source, index and indexer
        Run the indexer
        """
        self.create_data_source()
        self.create_index()
        self.create_indexer()
        self.run_indexer()
        self.count_documents()

    def delete_search_service(self):
        """When you want to change the index, delete everything first
        """

        delete_datasource_url = (
            self.url
            + f"datasources/{self.data_source_name}?"
            + self.api_version
        )
        response = requests.delete(delete_datasource_url, headers=self.headers)
        if response.status_code == 204:
            LOGGER.info("SUCCESSFULL DELETE request to %s. Returned status code %s",delete_datasource_url, response.status_code)
        else:
            LOGGER.info("UNSUCCESSFULL DELETE request to %s. Returned status code %s",delete_datasource_url, response.status_code)
            LOGGER.info("Body: %s", response.json())


        delete_index_url = (
            self.url
            + f"indexes/{self.index_name}?"
            + self.api_version
        )
        response = requests.delete(delete_index_url, headers=self.headers)
        if response.status_code == 204:
            LOGGER.info("SUCCESSFULL DELETE request to %s. Returned status code %s",delete_index_url, response.status_code)
        else:
            LOGGER.info("UNSUCCESSFULL DELETE request to %s. Returned status code %s",delete_index_url, response.status_code)
            LOGGER.info("Body: %s", response.json())


        delete_indexer_url = (
            self.url
            + f"indexers/{self.indexer_name}?"
            + self.api_version
        )
        response = requests.delete(delete_indexer_url, headers=self.headers)

        if response.status_code == 204:
            LOGGER.info("SUCCESSFULL DELETE request to %s. Returned status code %s",delete_indexer_url, response.status_code)
        else:
            LOGGER.info("UNSUCCESSFULL DELETE request to %s. Returned status code %s",delete_indexer_url, response.status_code)
            LOGGER.info("Body: %s", response.json())

    def check_indexer_status(self):
        check_indexer_status_url = (
            self.url
            + f"indexers/{self.indexer_name}/status?"
            + self.api_version
        )
        sleep(5)
        while requests.get(check_indexer_status_url, headers=self.headers).json().get('lastResult')['status'] == 'inProgress':
            LOGGER.info('Indexer in progress. Sleeping for 5 seconds. Zzzzzz...')

            sleep(5)
        if requests.get(check_indexer_status_url, headers=self.headers).json().get('lastResult')['status'] == 'success':
            LOGGER.info('Indexer created correctly, you can start your search queries')
            LOGGER.info("""\n_____.___.                                    __   ._.
\__  |   | ____  __ __  _______  ____   ____ |  | _| |
 /   |   |/  _ \|  |  \ \_  __ \/  _ \_/ ___\|  |/ / |
 \____   (  <_> )  |  /  |  | \(  <_> )  \___|    < \|
 / ______|\____/|____/   |__|   \____/ \___  >__|_ \__
 \/                                        \/     \/\/""")
        else:
            LOGGER.warning('Indexer did not finish with status "success".')

    def count_documents(self):
        count_docs_url = (
            self.url
            + f"indexes/{self.index_name}/docs/$count?"
            + self.api_version
        )
        response = requests.get(count_docs_url, headers=self.headers)
        LOGGER.warning('Counted %s documents in index %s.', response.text, self.index_name)


if __name__ == "__main__":
    search_service = SearchService()
    search_service.delete_search_service()
    search_service.setup_search_service()
    
