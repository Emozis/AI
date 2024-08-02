import os
import json
from pathlib import Path
from pymongo import MongoClient
from naraetool.main_logger import logger 
from naraetool.config import config
from urllib.parse import quote_plus
from bson import ObjectId

# 사용자 정의 JSON 인코더 클래스
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

class MongoDB:
    def __init__(self, config):
        # 백업 저장소 설정
        self.save_path = config["backup_path"]

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
        with open(self.save_path, "w", encoding="utf-8") as json_file:
            json.dump(self.documents, json_file, cls=JSONEncoder, ensure_ascii=False, indent=4)

    def create(self, document):
        self.collection.insert_one(document)
        self._backup()

        logger.debug(f"➕ Create Document: {document}")

    def update(self, query, new_document):
        result = self.collection.update_one(
            query, 
            {"$set": new_document}
        )
        
        if result.matched_count > 0:
            logger.debug(f"✔️ Update Document: {new_document}")
            self._backup()
        else:
            logger.warning("🚨 Update failed due to no matching documents")

    def delete(self, document):
        result = self.collection.delete_one(document)

        if result.deleted_count > 0:
            logger.debug(f"➖ Delete Document: {document}")
            self._backup()
        else:
            logger.warning("🚨 Delete failed due to no matching documents")

        

mongo = MongoDB(config.mongodb)