import logging

from pymongo import MongoClient, errors


class MongodbManager:
    def __init__(self, host="localhost", port=27017, bd_name="drink_dispenser"):
        self.logger = logging.getLogger("mongo")
        self.host = host
        self.port = port
        self.mongo_client = self.create_connection()
        self.mongo_db = self.mongo_client[bd_name]

    def create_connection(self):
        try:
            self.logger.debug(
                f"Creating MongoDB connection. Host: {self.host}, Port: {self.port}"
            )
            client = MongoClient(host=self.host, port=self.port)
            client.server_info()
            return client
        except errors.ConnectionFailure as e:
            self.logger.exception(f"Could not connect to MongoDB server - {e}")
            raise

    def get_collection(self, name):
        self.logger.debug(f"Getting MongoDB collection {name}")
        try:
            coll_ist = self.mongo_db.list_collection_names()
            if name in coll_ist:
                return self.mongo_db.get_collection(name)
            return self.mongo_db.create_collection(name)
        except errors.PyMongoError as e:
            self.logger.error(f"Collection could not be fetched - {e}")
            return None

    def insert_one(self, data, coll_name):
        self.logger.debug(f"Inserting document into '{coll_name}'")
        collection = self.get_collection(coll_name)
        try:
            id_code = collection.insert_one(data)
        except errors.PyMongoError as e:
            self.logger.error(
                f"Document {data} could not be inserted into '{coll_name}' - {e}"
            )
            return None
        return str(id_code.inserted_id)

    def insert_many(self, data, coll_name):
        self.logger.debug(f"Inserting many documents into {coll_name}")
        collection = self.get_collection(coll_name)
        try:
            id_list = collection.insert_many(data)
        except errors.PyMongoError as e:
            self.logger.error(
                f"Documents {data} could not be inserted into '{coll_name}' - {e}"
            )
            return None
        return id_list

    def find_document(self, coll_name, query, find_one=False):
        """
        Parameters:
            coll_name (str): name of the collection
            query (dict): to select documents that meet the query
            find_one (bool): True to find just one document False to find all
        Return:
            Document/s if document exists else None
        """
        self.logger.debug(
            f"Finding document from '{coll_name}' using following query {query}"
        )
        collection = self.mongo_db[coll_name]
        try:
            if find_one:
                return collection.find_one(query)
            else:
                return collection.find(query)
        except errors.PyMongoError as e:
            self.logger.error(
                f"Document could not be found using following query {query}- {e}"
            )
            return None

    def update_one(self, coll_name, query, new_values):
        """
        Parameters:
            coll_name (str): name of the collection
            query (dict): to get specific document
            new_values (dict): whose keys must be field to updated and its new value
        Return:
            Number of rows updated if some document was updated else None
        """
        collection = self.mongo_db[coll_name]
        try:
            new_rows_modified = collection.update_one(
                query, {"$set": new_values}
            ).modified_count
            return new_rows_modified
        except errors.PyMongoError as e:
            self.logger.error(
                f"Document could not be updated using following query {query}- {e}"
            )
            return None

    def remove_one(self, coll_name, query):
        """
        Parameters:
            coll_name (str): name of the collection
            query (dict): to get specific document
        Return:
            Number of rows removed if some document was removed else None
        """
        self.logger.debug(
            f"Removing document from MongoDB using following query {query}"
        )
        try:
            collection = self.mongo_db[coll_name]
            rows_deleted = collection.delete_one(query).deleted_count
            return rows_deleted
        except errors.PyMongoError as e:
            self.logger.error(
                f"Document could not be removed using following query {query}- {e}"
            )
            return None