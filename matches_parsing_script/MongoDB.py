from pymongo import MongoClient, UpdateOne
import pymongo.errors


class MongoDBWorker:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_mongo_connection(self):
        try:
            # Менять соединение с монгой
            client = MongoClient(self.host, self.port)
            db = client.dota_db
            return client, db
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
