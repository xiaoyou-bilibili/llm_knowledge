from embedding.llm.base import BaseLLM
from base import Config
import openai


class Openapi(BaseLLM):
    def __init__(self, config: 'Config'):
        self.__config = config
        openai.api_base = config.openapi_base
        openai.api_key = config.openapi_key
        self.__context = []

    def embedding(self, text: str) -> dict[dict]:
        embedding = openai.Embedding.create(model="text-embedding-ada-002", input=text)
        return embedding.data[0].embedding

    def ask(self, query: str, context: str) -> str:
        messages = [
            {"role": "system", "content": f'你是一个乐于助人的作者，你需要从下文中提取有用的内容来解答用户提出的问题，不能回答不在下文提到的内容，回答请以我的视角回答：\n\n{context}'}
        ]
        self.__context.append({"role": "user", "content": query})
        messages.extend(self.__context)
        print(messages)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        answer = response.choices[0].message.content
        print("使用的tokens：", response.usage.total_tokens)
        self.__context.append({"role": "assistant", "content": answer})
        return answer

    def clear(self):
        self.__context = []