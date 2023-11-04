from langchain.document_loaders import BraveSearchLoader
from haystack.nodes import BaseComponent
from haystack.schema import Document
from typing import Optional
from pymongo import MongoClient

brave_endpoint = "https://api.search.brave.com/res/v1/web/search?q="
brave_api_key = "BSAt2nmuC57jmjrGEY9-JNAyAHTU6Z5"

class MongoFetcher(BaseComponent):
    outgoing_edges = 1

    def __init__(self, password):
        self.mongoClient = MongoClient(f"mongodb+srv://hackuser:{password}@hack-cluster.aiglafg.mongodb.net/?retryWrites=true&w=majority")

    def run(self):
        db = self.mongoClient['hack']
        collection = db['hack']
        docs = []
        for doc in collection.find():
            docs.extend([Document(content=doc[key]['text'], meta={'title': key, 'url': doc[key]['url']}) for key in doc if key != '_id'])
        output = {"documents": docs}
        return output, "output_1"

    def run_batch(self):
        pass
