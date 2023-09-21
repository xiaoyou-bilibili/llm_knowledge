# 默认大模型
class BaseLLM:
    # 把文本编码为特征向量数据
    def embedding(self, text: str) -> dict[dict]:
        pass

    # 询问ai问题并获得解答
    def ask(self, query: str, context: str) -> str:
        pass

    # 清除上下文
    def clear(self):
        pass