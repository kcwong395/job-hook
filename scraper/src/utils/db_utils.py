import logging
from typing import List, Optional

import pymongo
import pymongo.results
import pymongo.database
import pymongo.errors


class DbUtils:
    _client = None
    _db = None
    _logger = logging.getLogger()

    @staticmethod
    def connect(db_name: str, username: str, password: str, host: str, port: str) -> pymongo.database.Database:
        """ This static func returns the db handler """
        if not DbUtils._db:
            DbUtils._client = pymongo.MongoClient("mongodb://" + username + ":" + password + "@" + host + ":" + port)
            DbUtils._db = DbUtils._client[db_name]
            DbUtils._logger.warning("Database connect created...")
        return DbUtils._db

    @staticmethod
    def get_collection(collection_name: str) -> pymongo.collection.Collection:
        if collection_name not in DbUtils._db.list_collection_names():
            DbUtils._logger.warning("Collection Name " + collection_name + " does not exist")
            DbUtils._logger.warning("Creating Collection " + collection_name)
        return DbUtils._db[collection_name]

    @staticmethod
    def insert(collection: pymongo.collection.Collection, document: any) -> Optional[pymongo.results.InsertOneResult]:
        res = None
        try:
            res = collection.insert_one(document.__dict__)
        except pymongo.errors.DuplicateKeyError:
            logging.error('Document id already exist and insertion of job: ' + str(document.__dict__) + ' failed')
        else:
            logging.info('Document with id: ' + str(res.inserted_id) + ' inserted')
        return res

    @staticmethod
    def insert_many(collection: pymongo.collection.Collection, documents: List[any]) -> None:
        for doc in documents:
            DbUtils.insert(collection, doc)
        return None

    @staticmethod
    def get_documents(collection: pymongo.collection.Collection) -> List[any]:
        return [doc for doc in collection.find()]

    @staticmethod
    def close():
        DbUtils._client.close()
        DbUtils._logger.warning("Database connect shutdowned...")

