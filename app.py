# encoding: utf-8
from flask import Flask, send_file, request
import io, os
from flask_cors import CORS
from flask_socketio import SocketIO
import time
from authlib.jose import jwt
# 蓝图
from .apps.users.views import user_dp
# 数据库
from .apps.db_model import db
# 迁移
from flask_migrate import Migrate

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
print(SECRET_KEY, os.getenv('DATA'))

lb = ['http://127.0.0.1']
socket = SocketIO(app, cors_allowed_origins='*', ping_timeout=5, ping_interval=1)
CORS(app, cors_allowed_origins='*')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATA')
# mysql配置

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@192.168.43.99:3307/xuwuChat'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/xw.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:agl001@127.0.0.1:3306/demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


# 注册蓝图
app.register_blueprint(user_dp)
number_lb = []   # 记录在线人数


@app.route('/')
def create_data():
    db.drop_all()
    db.create_all()
    return '数据库创建成功.'


online_number = 0   # 在线人数


@socket.on('connect')
def connect():
    global online_number
    online_number += 1
    sid = request.sid
    print(f'{sid}上线了...当前在线人数：{online_number}')
    data = {
        'number': online_number,
    }
    socket.emit('connect', data)
    # 加入房间


@socket.on('disconnect')
def disconnect():
    global online_number
    online_number -= 1
    print(f'当前在线人数：{online_number}')
    data = {
        'number': online_number,
    }
    socket.emit('disconnect', data)


@socket.on('msg')
def msg(msg):
    print(msg)
    m = msg.get('msg')
    t = msg.get('token')
    message = m.encode('utf-8')
    message = message.decode('utf-8')
    # print(msg)
    # 返回自己的消息
    socket.emit('me', message)
    # ai回复
    time.sleep(1)

    msg = """好的，这里是一个简单的 Flask 应用程序，它可以在浏览器中显示 "Hello World!"。
```python
from flask import Flask
from app import SECRET_KEY

app = Flask(__name__)

@app.route('/')
def hello_world():
    a = 1
    b = 2
    print("hello 哈哈哈 123", a+b)
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

在这个例子中，我们导入了 Flask 类并创建了一个应用程序实例。我们使用装饰器 @app.route('/') 来定义一个路由，它指定了当用户访问应用程序的根 URL 时要执行的函数。在这个例子中，我们的函数名是 hello_world()，它返回一个简单的字符串 "Hello World!"。

最后，我们在 if __name__ == '__main__': 语句块中调用 app.run() 方法来启动应用程序。这将在本地计算机上启动一个 Web 服务器，并使应用程序在其中运行。

您可以在命令行中运行这个应用程序，然后在浏览器中输入 http://localhost:5000/ 来查看它的输出。"""
    # f.close()
    msg = "# 哈哈哈 \n *** \n> 完毕"
    socket.emit('ai', msg)


# 社区交流
@socket.on('community')
def community(msg):
    print(msg)
    m = msg.get('msg')
    t = msg.get('token')
    message = m.encode('utf-8')
    message = message.decode('utf-8')

    # 判断一下是谁发来的消息，通过判断token
    if t:
        d = jwt.decode(t, SECRET_KEY)  # 解密令牌
        print(d)
        data = {'message': message, 'username': d.get('user_id')}
        socket.emit('communitys', data)
    else:
        print('没有登录')
        data = {'message': message, 'username': '游客'}
        socket.emit('communitys', data)


# 测试blob图片返回
@app.route('/img')
def testImg():
    files = r'C:\Users\罗远生\Desktop\untitled\a.mp4'
    with open(files, 'rb') as f:
        data = f.read()
        by_data = io.BytesIO(data)

    # mimetype设置返回类型，迷惑对方
    # return Response(by_data, mimetype='image/png')
    return send_file(by_data, mimetype='image/png')


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=8000, debug=True)