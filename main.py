from web import app
from embedding import Embedding
from base import EMBEDDING

if __name__ == '__main__':
    # 配置相关服务
    app.config[EMBEDDING] = Embedding()
    # 运行flask
    app.run(host='0.0.0.0', port=7001)
