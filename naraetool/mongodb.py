import os
from pymongo import MongoClient
from naraetool.main_logger import logger 
from naraetool.config import config
from urllib.parse import quote_plus


class MongoDB:
    def __init__(self, config):
        self.save_path = "./data/mongodb_backup.json"

        # 기본 설정값
        host = config["host"]
        # port = config["port"]         # atlas로 관리하여 제외
        db = config.get("db", None)
        collection = config.get("collection", None)

        username = quote_plus(os.getenv(config["userKey"], ""))
        password = quote_plus(os.getenv(config["pwdKey"], ""))
        
        # URI 생성
        # uri = f"mongodb://{username}:{password}@{host}:{port}/{db}"         # atlas로 관리하여 제외
        uri = f"mongodb+srv://{username}:{password}@{host}"
        
        # 클라이언트 유효성 검사
        try:
            # 클라이언트 생성
            self.client = MongoClient(uri)
            self.db_list = self.client.list_database_names()
            
            # db, collection 생성
            self.db = self._get_db(db)
            self.collection = self._get_collection(collection)
            
            # 로거
            logger.info(f"클라이언트 생성 완료")
        except:
            logger.error("연결정보가 올바르지 않습니다. URI 정보들을 다시 확인해주세요.(format=mongodb+srv://{username}:{password}@{host})")

    def _get_db(self, db_name):
        try:
            db = self.client[db_name]
            self.collection_list = db.list_collection_names()
        except:
            logger.error(f"데이터베이스 목록을 다시 확인하세요 - {self.db_list}")
        
        return db

    def _get_collection(self, collection_name):
        try:
            collection = self.db[collection_name]
        except:
            logger.error(f"컬렉션 목록을 다시 확인하세요 - {self.collection_list}")
        
        return collection

    @property
    def documents(self):
        data = list(self.collection.find())

        return data
    
    def _backup(self):
        self.documents.to_json(
            self.save_path, 
            orient="records", 
            date_format="iso", 
            indent=4, 
            index=False,
            force_ascii=False
        )

    def create(self, document):
        self.collection.insert_one(document)
        self._backup()

    def update(self, query, new_doc):
        self.collection.update_one(
            query, 
            {"$set": new_doc}
        )
        self._backup()

    def delete(self, document):
        self.collection.delete_one(document)
        self._backup()
        

mongo = MongoDB(config.mongodb)