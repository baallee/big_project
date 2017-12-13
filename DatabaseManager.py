from pymongo import MongoClient

class DatabaseManager:
    def __init__(self):
        #init db connection
        client = MongoClient('localhost', 27017)
        self.db = client.big_project