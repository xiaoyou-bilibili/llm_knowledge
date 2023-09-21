from bs4 import BeautifulSoup
import requests
from flask import Flask, request, Response, render_template
import json
from embedding import Embedding
from base import EMBEDDING

# 初始化flaskAPP
app = Flask(__name__)


# 返回JSON字符串
def return_json(data):
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 网页爬取
@app.route('/content/web', methods=['POST'])
def content_web():
    data = request.get_json()
    # 获取网页内容
    response = requests.get(data['url'])
    # 创建BeautifulSoup对象
    content = BeautifulSoup(response.text, 'html.parser')
    if data["id"] != "":
        content = content.find(id=data['id'])
    # 返回json类型字符串
    return return_json({"content": content.get_text()})


# 普通文本
@app.route('/content/text', methods=['POST'])
def content_text():
    embedding: Embedding = app.config[EMBEDDING]
    data = request.get_json()
    embedding.add_text(data["content"], data["url"])
    # 返回json类型字符串
    return return_json(data)


# 查询数据
@app.route('/db/query', methods=['GET'])
def db_query():
    embedding: Embedding = app.config[EMBEDDING]
    query = request.args.get('query')
    try:
        size = int(str(request.args.get('size')))
    except (ValueError, TypeError):
        size = 1
    if query is None or query == "":
        return return_json({
            "msg": "请输入query"
        })
    # 返回json类型字符串
    return return_json(embedding.query_text(query, size))


# 查询数据
@app.route('/db/get', methods=['GET'])
def db_get():
    embedding: Embedding = app.config[EMBEDDING]
    try:
        no = int(str(request.args.get('page')))
        size = int(str(request.args.get('limit')))
    except (ValueError, TypeError):
        no = 1
        size = 20
    data = embedding.get_data(no, size)
    data["code"] = 0
    # 返回json类型字符串
    return return_json(data)


# 查询数据
@app.route('/db/delete', methods=['GET'])
def db_delete():
    embedding: Embedding = app.config[EMBEDDING]
    embedding.delete_data(str(request.args.get('id')))
    # 返回json类型字符串
    return return_json({})


# 询问问题
@app.route('/chat/ask', methods=['POST'])
def ask_question():
    embedding: Embedding = app.config[EMBEDDING]
    data = request.get_json()
    # 返回json类型字符串
    return return_json({
        "answer": embedding.ask_question(data["question"])
    })


# 清除上下文
@app.route('/chat/clear', methods=['POST'])
def clear_ask():
    embedding: Embedding = app.config[EMBEDDING]
    embedding.clear_question()
    return return_json({})


# 主页显示HTML
@app.route('/', methods=['GET'])
def index():
    return render_template('content.html')
