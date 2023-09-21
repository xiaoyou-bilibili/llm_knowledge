import chromadb
import uuid
from chromadb.utils import embedding_functions
from base import Config


class ChromadbDb:
    def __init__(self):
        self.__config = Config()
        self.__chroma_client = chromadb.PersistentClient(path="db")
        self.__collection = self.__chroma_client.get_or_create_collection(
            name="embedding",
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_base=self.__config.openapi_base,
                api_key=self.__config.openapi_key,
                model_name="text-embedding-ada-002",
            ))

    # 添加文本
    def add_text(self, text: str, embedding: dict[dict], meta: dict):
        self.__collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[meta],
            ids=[uuid.uuid4().hex]
        )

    def query_text(self, query: str, result: int):
        results = self.__collection.query(
            query_texts=[query],
            n_results=result
        )
        return results

    def get_data(self, no: int, size: int) -> [int, dict]:
        count = self.__collection.count()
        result = self.__collection.get(limit=size, offset=(no - 1) * size)
        return count, result

    def delete_data(self, ids: list[str]):
        self.__collection.delete(ids=ids)
