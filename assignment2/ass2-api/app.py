from flask import Flask, request, jsonify
from flasgger import Swagger
from groq import Groq
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # 导入 CORS

app = Flask(__name__)
CORS(app)  # 启用 CORS
swagger = Swagger(app)

# 配置 MySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/mse800'  # 替换 db_name 为你的数据库名
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义模型
class CookList(db.Model):
    __tablename__ = 'cook_list'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(4000), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)  # 默认当前时间

    # 添加 to_dict 方法
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'create_date': self.create_date.isoformat()  # 转换为 ISO 格式字符串
        }

# 创建数据库表（如果需要）
with app.app_context():
    db.create_all()

# 登录路由
@app.route('/login', methods=['POST'])
def login():
    """
    用户登录
    ---
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: 用户名
      - name: password
        in: body
        type: string
        required: true
        description: 密码
    responses:
      200:
        description: 登录成功
      401:
        description: 用户名或密码错误
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 这里可以添加验证逻辑
    if username == 'admin' and password == 'password':  # 示例验证
        return jsonify({"message": "登录成功"}), 200
    else:
        return jsonify({"message": "用户名或密码错误"}), 401

# 在 assignment2/ass2-api/app.py 中添加以下代码

@app.route('/getFoodSmart', methods=['POST'])
def getFoodSmart():
    """
    获取食物智能建议
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            ingredients:
              type: string
              description: 食材
              example: "鸡肉, 米饭, 胡萝卜"
            instructions:
              type: string
              description: 制作步骤
              example: "将鸡肉煮熟，加入米饭和胡萝卜，搅拌均匀。"
    responses:
      200:
        description: 返回食材和步骤
        schema:
          type: object
          properties:
            message:
              type: string
              description: 菜谱和详细步骤
    """
    data = request.json
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')
    
    client = Groq(
        api_key="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",
    )

    # 将 ingredients 和 instructions 放入 content 中
    content = f"根据以下食材和步骤生成菜谱：食材：{ingredients}，制作步骤：{instructions}。"\
        "请以Markdown格式返回菜谱和详细步骤。"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )

    titles = chat_completion.choices[0].message.content

    print(titles)



    return jsonify({"message": titles}), 200

@app.route('/saveCookMessage', methods=['POST'])
def saveCookMessage():
    """
    保存烹饪消息
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            userId:
              type: string
              description: 用户ID
              example: "user123"
            cookMessage:
              type: string
              description: 烹饪消息
              example: "今天的晚餐是意大利面。"
    responses:
      200:
        description: 消息保存成功
      400:
        description: 请求参数错误
    """
    data = request.json
    user_id = data.get('userId')
    cook_message = data.get('cookMessage')

    if not user_id or not cook_message:
        return jsonify({"error": "缺少 userId 或 cookMessage"}), 400

    new_message = CookList(user_id=user_id, message=cook_message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "烹饪消息保存成功"}), 200

# 新增方法
@app.route('/cook_list/<userId>', methods=['GET'])
def get_cook_list(userId):
    """
    根据 userId 查询 cook_list 表中的数据，按照 create_date 倒序排列
    ---
    parameters:
      - name: userId
        in: path
        type: string  # 修改为 string 类型
        required: true
        description: 用户 ID
    responses:
      200:
        description: 成功返回 cook_list 数据
        schema:
          type: array
          items:
            $ref: '#/definitions/Cook'
    """
    cook_list = CookList.query.filter_by(user_id=userId).order_by(CookList.create_date.desc()).all()
    return jsonify([cook.to_dict() for cook in cook_list])  # 这里调用 to_dict 方法

if __name__ == '__main__':
    app.run(debug=True)
