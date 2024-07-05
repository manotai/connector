from elasticsearch import Elasticsearch
from typing import Dict, List
import os

from connector.elastic.queries import more_like_this_query

ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', 'test')
ELASTIC_HOST = os.environ.get('ELASTIC_HOST', 'localhost')


class ElasticsearchWrapper:
    """
        A wrapper class for interacting with an Elasticsearch cluster.

        This class provides methods for creating, reading, updating, and deleting documents
        in an Elasticsearch index, as well as checking for index existence and creating indices.

        :param host: The hostname of the Elasticsearch server.
        :type host: str
        :param port: The port of the Elasticsearch server.
        :type port: int
    """

    def __init__(self, host='localhost', port=9200):
        """
            Initializes the ElasticsearchWrapper instance.

            :param host: The hostname of the Elasticsearch server.
            :type host: str
            :param port: The port of the Elasticsearch server.
            :type port: int
        """

        self.client = Elasticsearch(f'http://{ELASTIC_HOST}:9200', basic_auth=('elastic', ELASTIC_PASSWORD))

    def create_document(self, index: str, body: Dict):
        """
            Creates a new document in the specified index.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param body: The document body to be indexed.
            :type body: dict
            :return: The response from Elasticsearch.
            :rtype: dict
        """
        return self.client.index(index=index, body=body)

    def get_document(self, index: str, body: Dict):
        """
            Retrieves a document from the specified index by its ID.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param body: The document body.
            :type body: dict
            :return: The retrieved document.
            :rtype: dict
        """
        return self.client.get(index=index, body=body)

    def update_document(self, index: str, body: Dict):
        """
            Updates an existing document in the specified index.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param body: The document body.
            :type body: dict
            :param body: The updated document body.
            :type body: dict
            :return: The response from Elasticsearch.
            :rtype: dict
        """
        return self.client.update(index=index, body={'doc': body})

    def delete_document(self, index: str, id_: str):
        """
            Deletes a document from the specified index by its ID.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param id_: The ID of the document to delete.
            :type id_: str
            :return: The response from Elasticsearch.
            :rtype: dict
        """
        return self.client.delete(index=index, id=id_)

    def index_exists(self, index: str):
        """
            Checks if the specified index exists.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :return: True if the index exists, False otherwise.
            :rtype: bool
        """
        return self.client.indices.exists(index=index)

    def create_index(self, index: str, body: Dict = None):
        """
            Creates a new index with the specified name and optional settings.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param body: The index settings and mappings.
            :type body: dict, optional
            :return: The response from Elasticsearch.
            :rtype: dict
        """
        self.client.indices.create(index=index, body=body)

    def more_like_this(self, index: str, fields: List[str], body: str) -> bool:
        """
            Searches for documents similar to the provided text in the specified fields.

            :param index: The name of the Elasticsearch index.
            :type index: str
            :param fields: The list of fields to search in.
            :type fields: list
            :param body: The text to find similar documents for.
            :type body: str
            :return: The response from Elasticsearch.
            :rtype: dict
        """
        query = more_like_this_query(body, fields)
        response = self.client.search(index=index, body=query)
        return response

