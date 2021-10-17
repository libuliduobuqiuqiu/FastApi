# -*- coding: utf-8 -*-

from pymongo.mongo_client import MongoClient
from setting import DB_NAME, MONGODB_URI


class MongoConnect:
    def __init__(self, col_name: str, db_name: str = DB_NAME):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[db_name]
        self.col = self.db[col_name]

    def insert(self, data):
        try:
            if isinstance(data, dict):
                self.col.insert_one(data)

            elif isinstance(data, list):
                self.col.insert_many(data)
        except Exception as e:
            raise Exception(f"插入异常:{e}")

    def read(self, condition: dict = None):
        if not condition:
            docs = self.col.find({}, {"_id": 0})

        else:
            docs = self.col.find(condition, {"_id": 0})

        return [doc for doc in docs]