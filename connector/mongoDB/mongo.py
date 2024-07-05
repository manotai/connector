from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict


class MongoDBClient:
    """
        A client class for interacting with a MongoDB database.

        This class provides methods for creating, reading, updating, and deleting documents
        in a specified MongoDB collection.

        :param database_name: The name of the MongoDB database.
        :type database_name: str
        :param collection_name: The name of the MongoDB collection.
        :type collection_name: str
        :param mongo_uri: The MongoDB connection URI.
        :type mongo_uri: str
    """
    def __init__(self, database_name: str, collection_name: str, mongo_uri: str):
        """
            Initializes the MongoDBClient instance.

            :param database_name: The name of the MongoDB database.
            :type database_name: str
            :param collection_name: The name of the MongoDB collection.
            :type collection_name: str
            :param mongo_uri: The MongoDB connection URI.
            :type mongo_uri: str
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def create_document(self, document: Dict) -> bool:
        """
           Creates a new document in the collection.

           :param document: The document to be created.
           :type document: dict
           :return: True if the document was created successfully.
           :rtype: bool
       """
        self.collection.insert_one(document)
        print("Document created successfully.")
        return True

    def read_document(self, query: Dict) -> Dict:
        """
            Reads a document from the collection based on the provided query.

            :param query: The query to find the document.
            :type query: dict
            :return: The found document or an empty dictionary if not found.
            :rtype: dict
        """
        try:
            document = self.collection.find_one(query)
            if document:
                return document
            else:
                print("Document not found.")
                return {}
        except PyMongoError as e:
            print(f"Error reading document: {e}")
            return {}

    def update_document(self, query: Dict, update: Dict) -> bool:
        """
           Updates a document in the collection based on the provided query.

           :param query: The query to find the document to update.
           :type query: dict
           :param update: The update to apply to the document.
           :type update: dict
           :return: True if the document was updated successfully, False otherwise.
           :rtype: bool
       """
        try:
            result = self.collection.update_one(query, {'$set': update})
            if result.modified_count > 0:
                print("Document updated successfully.")
                return True
            else:
                print("No documents updated.")
                return False
        except PyMongoError as e:
            print(f"Error updating document: {e}")
            return False

    def delete_document(self, query: Dict) -> bool:
        """
            Deletes a document from the collection based on the provided query.

            :param query: The query to find the document to delete.
            :type query: dict
            :return: True if the document was deleted successfully, False otherwise.
            :rtype: bool
        """
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print("Document deleted successfully.")
                return True
            else:
                print("No documents deleted.")
                return False
        except PyMongoError as e:
            print(f"Error deleting document: {e}")
            return False

    def close_connection(self):
        self.client.close()
        print("mongoDB connection closed.")


