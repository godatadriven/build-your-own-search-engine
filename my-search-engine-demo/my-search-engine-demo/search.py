# Setup a search service on an azure blob container
import requests
import os
from azure.core.exceptions import HttpResponseError
import logging
from time import sleep
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SearchService:
    """Index Azure Blob with Azure Cognitive Search
    """
    def __init__(self):
        """Initialize required configurations
        Service name: name of search service
        API key: secret of search service
        API version: version of search API
        """
        self.endpoint = os.environ["SEARCH_ENDPOINT"]
        self.headers = {
            "Content-Type": "application/json",
            "api-key": f"{os.environ['ACS_API_KEY']}",
        }
        self.api_version = "api-version=2020-06-30"

    def create_data_source(self):
        """Setup the blob
        connectionString: connection string from storage account
        container: name of container in storage account
        """
        container_name = "covid-news"
        data_source_schema = {
            "name": "covid-19-datasource",
            "type": "azureblob",
            "credentials": {"connectionString": f"{os.environ['PLAYGROUND_CONN_STR']}"},
            "container": {"name": f"{container_name}"},
        }

        data_source_url = (
            self.endpoint
            + "datasources?"
            + self.api_version
        )

        try:
            requests.post(
                data_source_url, headers=self.headers, json=data_source_schema
            )
            sleep(3)
            logger.info('Created datasource: %s', requests.get(
                data_source_url, headers=self.headers
            ).json())
           
            
        except HttpResponseError:
            logger.info('Data source already exists')
            

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
            self.endpoint
            + "indexes?"
            + self.api_version
        )

        try:
            requests.post(index_url, headers=self.headers, json=index_schema)
            sleep(3)
            index_url = (
            self.endpoint
            + "indexes/covid-19-index?"
            + self.api_version
        )
            logger.info('Created index: %s', requests.get(
                index_url, headers=self.headers
            ).json())
           

        except HttpResponseError:
            logger.info("Index already exists")

    def create_indexer(self):
        """Create an indexer that will index the files in the Blob
        """
        indexer_schema = {
            "name": "covid-19-indexer",
            "dataSourceName": "covid-19-datasource",
            "targetIndexName": "covid-19-index",
            "parameters": {
                "configuration": {
                    "parsingMode": "jsonLines",
                    "dataToExtract": "contentAndMetadata",
                }
            },
        }
        indexer_url = (
            self.endpoint
            + "indexers?"
            + self.api_version
        )

        try:
            requests.post(indexer_url, headers=self.headers, json=indexer_schema)
            sleep(3)
            logger.info('Created indexer: %s', requests.get(
                indexer_url, headers=self.headers
            ).json())
           

        except HttpResponseError:
            logger.info("Indexer already exists")


    def run_indexer(self):
        """Run the indexer to index the files in the blob
        """
        run_indexer_url = (
            self.endpoint
            + "indexers/covid-19-indexer/run?"
            + self.api_version
        )
        requests.post(run_indexer_url, headers=self.headers)
        logger.info("Started indexer")

    def setup_search_service(self):
        """Setup the search service:
        Create the data source, index and indexer
        Run the indexer
        """
        self.create_data_source()
        self.create_index()
        self.create_indexer()
        self.run_indexer()
        self.check_indexer_status()
        
    def check_indexer_status(self):
        check_indexer_status_url = (
            self.endpoint
            + "indexers/covid-19-indexer/status?"
            + self.api_version
        )
        sleep(5)
        while requests.get(check_indexer_status_url, headers=self.headers).json().get('lastResult')['status'] == 'inProgress':
            logger.info('Indexer in progress. Sleeping for 5 seconds. Zzzzzz...')

            sleep(5)
        if requests.get(check_indexer_status_url, headers=self.headers).json().get('lastResult')['status'] == 'success':
            logger.info('Indexer created correctly, you can start your search queries')
            logger.info("""\n_____.___.                                    __   ._.
\__  |   | ____  __ __  _______  ____   ____ |  | _| |
 /   |   |/  _ \|  |  \ \_  __ \/  _ \_/ ___\|  |/ / |
 \____   (  <_> )  |  /  |  | \(  <_> )  \___|    < \|
 / ______|\____/|____/   |__|   \____/ \___  >__|_ \__
 \/                                        \/     \/\/""")
        else:
            logger.warning('Indexer did not finish with status "success".')



    def delete_search_service(self):
        """When you want to change the index, delete everything first
        """

        delete_datasource_url = (
            self.endpoint
            + "datasources/covid-19-datasource?"
            + self.api_version
        )
        requests.delete(delete_datasource_url, headers=self.headers)

        delete_index_url = (
            self.endpoint
            + "indexes/covid-19-index?"
            + self.api_version
        )
        requests.delete(delete_index_url, headers=self.headers)

        delete_indexer_url = (
            self.endpoint
            + "indexers/covid-19-indexer?"
            + self.api_version
        )
        requests.delete(delete_indexer_url, headers=self.headers)

if __name__ == "__main__":
    search_service = SearchService()
    search_service.delete_search_service()
    search_service.setup_search_service()