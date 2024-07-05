import boto3
from botocore.exceptions import ClientError
from typing import Dict


class DynamoDBClient:
    def __init__(self, table_name: str, region: str, aws_access_key_id: str, aws_secret_access_key: str):
        """
                Initializes a DynamoDB client.

                :param table_name: The name of the DynamoDB table.
                :type table_name: str
                :param region: The AWS region where the table is hosted.
                :type region: str
                :param aws_access_key_id: The AWS access key ID.
                :type aws_access_key_id: str
                :param aws_secret_access_key: The AWS secret access key.
                :type aws_secret_access_key: str
        """
        self.table_name: str = table_name
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=region,
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key)
        self.table = self.dynamodb.Table(table_name)

    def create_item(self, item_data: Dict) -> bool:
        """
                Creates a new item in the DynamoDB table.

                :param item_data: The data of the item to create.
                :type item_data: dict
                :return: True if the item was created successfully, False otherwise.
                :rtype: bool
        """
        try:
            self.table.put_item(Item=item_data)
            print(f"Item created successfully in table {self.table_name}")
            return True
        except ClientError as e:
            print(f"Error creating item: {e}")

    def get_item(self, key):
        """
            Retrieves an item from the DynamoDB table.

            :param key: The key of the item to retrieve.
            :type key: dict
            :return: The retrieved item, or None if the item was not found.
            :rtype: dict
        """
        try:
            response = self.table.get_item(Key=key)
            item = response.get('Item')
            return item
        except ClientError as e:
            print(f"Error getting item: {e}")

    def update_item(self, key, update_expression, expression_attribute_values):
        """
            Updates an existing item in the DynamoDB table.

            :param key: The key of the item to update.
            :type key: dict
            :param update_expression: The update expression specifying the attributes to update.
            :type update_expression: str
            :param expression_attribute_values: The values for the update expression.
            :type expression_attribute_values: dict
            :return: True if the item was updated successfully, False otherwise.
            :rtype: bool
        """
        try:
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            print(f"Item updated successfully in table {self.table_name}")
        except ClientError as e:
            print(f"Error updating item: {e}")

    def delete_item(self, key):
        """
            Deletes an item from the DynamoDB table.

            :param key: The key of the item to delete.
            :type key: dict
            :return: True if the item was deleted successfully, False otherwise.
            :rtype: bool
        """
        try:
            self.table.delete_item(Key=key)
            print(f"Item deleted successfully from table {self.table_name}")
        except ClientError as e:
            print(f"Error deleting item: {e}")
