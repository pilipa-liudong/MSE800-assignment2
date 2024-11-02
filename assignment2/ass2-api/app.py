from flask import Flask, request, jsonify
from flasgger import Swagger
from groq import Groq
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  

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
            'create_date': self.create_date.isoformat(),  # 转换为 ISO 格式字符串
            'message': self.message  # 添加 message 字段
        }

# 创建数据库表（如果需要）
with app.app_context():
    db.create_all()

# 登录路由
@app.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: Username
      - name: password
        in: body
        type: string
        required: true
        description: Password
    responses:
      200:
        description: Login successful
      401:
        description: Username or password incorrect
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
    get food references from AI
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
              description: Ingredients
              example: "Chicken, Rice, Carrots"
            instructions:
              type: string
              description: Cooking instructions
              example: "Cook the chicken, add rice and carrots, and stir well."
    responses:
      200:
        description: Returns ingredients and instructions
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
    Save cooking message
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
              description: User ID
              example: "user123"
            cookMessage:
              type: string
              description: Cooking message
              example: "Today's dinner is spaghetti."
    responses:
      200:
        description: Message saved successfully
      400:
        description: Request parameter error
    """
    data = request.json
    user_id = data.get('userId')
    cook_message = data.get('cookMessage')

    if not user_id or not cook_message:
        return jsonify({"error": "no userId 或 cookMessage"}), 400

    new_message = CookList(user_id=user_id, message=cook_message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "烹饪消息保存成功"}), 200

# 新增方法
@app.route('/cook_list/<userId>', methods=['GET'])
def get_cook_list(userId):
    """
    Query the cook_list table based on userId, ordered by create_date in descending order
    ---
    parameters:
      - name: userId
        in: path
        type: string  # Changed to string type
        required: true
        description: User ID
    responses:
      200:
        description: Successfully returns cook_list data
        schema:
          type: array
          items:
            $ref: '#/definitions/Cook'
    """
    cook_list = CookList.query.filter_by(user_id=userId).order_by(CookList.create_date.desc()).all()
    return jsonify([cook.to_dict() for cook in cook_list])  # 这里调用 to_dict 方法

# 新增方法
@app.route('/cook_list/<int:id>', methods=['DELETE'])
def delete_cook_list(id):
    """
    Delete data from the cook_list table based on id
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Cooking message ID
    responses:
      200:
        description: Successfully deleted cooking message
      404:
        description: Cooking message not found
    """
    cook_message = CookList.query.get(id)  # 根据 ID 查询烹饪消息

    if not cook_message:
        return jsonify({"error": "Cooking message not found"}), 404

    db.session.delete(cook_message)  # Delete cooking message
    db.session.commit()

    return jsonify({"message": "Successfully deleted cooking message"}), 200

if __name__ == '__main__':
    app.run(debug=True)
