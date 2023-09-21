from embedding.llm.openapi import Openapi
from embedding.vectordb.chromadb import ChromadbDb
from base.config import Config


class Embedding:
    def __init__(self):
        self.__config = Config()
        self._llm = Openapi(self.__config)
        self.__db = ChromadbDb()

    # 添加新文本
    def add_text(self, content: str, url: str):
        embedding = self._llm.embedding(content)
        self.__db.add_text(content, embedding, {"url": url})

    # 文本查询
    def query_text(self, query: str, size: int):
        return self.__db.query_text(query, size)

    # 获取数据
    def get_data(self, no: int, size: int):
        total, data = self.__db.get_data(no, size)
        data_list = []
        for i in range(len(data["ids"])):
            data_list.append({
                "id": data["ids"][i],
                "content": data["documents"][i],
                "url": data["metadatas"][i]["url"],
            })
        return {
            "count": total,
            "data": data_list
        }

    # 删除数据
    def delete_data(self, ids: str):
        self.__db.delete_data(ids.split(","))

    # 询问问题
    def ask_question(self, text: str):
        content = self.__db.query_text(text, 1)
        documents = content.get('documents')
        if len(documents) > 0:
            return self._llm.ask(query=text, context=documents[0])
        return ""
        # if content.get()
        # self._llm.ask(text)

    # 清除上下文
    def clear_question(self):
        self._llm.clear()
