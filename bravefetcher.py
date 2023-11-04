from langchain.document_loaders import BraveSearchLoader
from haystack.nodes import BaseComponent
from haystack.schema import Document
from typing import Optional
from newspaper import Article
import requests

brave_endpoint = "https://api.search.brave.com/res/v1/web/search?q="
brave_api_key = "BSAt2nmuC57jmjrGEY9-JNAyAHTU6Z5"

class BraveFetcher(BaseComponent):
    outgoing_edges = 1

    def __init__(self, last_k: Optional[int] = 25):
        self.last_k = last_k

    def run(self, last_k: Optional[int] = None):
        if last_k is None:
            last_k = self.last_k

        loader = BraveSearchLoader(
            query="uk income tax", api_key=brave_api_key, search_kwargs={"count": 10}
        )
        docs = loader.load()
        articles = [doc.metadata['link'] for doc in docs[:last_k] if "gov.uk" in doc.metadata['link']]

        docs = []
        for url in articles:
            try:
                article = Article(url)
                article.download()
                article.parse()
                docs.append(Document(content=article.text, meta={'title': article.title, 'url': url}))
            except:
                print(f"Couldn't download {url}, skipped")

        output = {"documents": docs}
        return output, "output_1"

    def run_batch(self):
        pass
