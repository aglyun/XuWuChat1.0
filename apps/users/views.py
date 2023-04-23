import os
from flask import Blueprint, request
from authlib.jose import jwt
from hashlib import blake2b
from faker import Faker

from apps.db_model import User, db

faker = Faker('zh_CN')   # 生成虚假信息

user_dp = Blueprint('user_dp', __name__)


# 注册接口
@user_dp.route('/register', methods=['POST'])
def register():
    # 测试中，暂时不要验证码，后期更新追加验证码验证功能
    email = request.get_json().get('email')
    pwd = request.get_json().get('pwd')
    pwd2 = request.get_json().get('pwd2')
    print(f"注册表单内容{email},{pwd}")
    # 从数据库中查询该用户是否已经注册
    db_e = User.query.filter_by(email=email).first()
    print(f'用户：{db_e}')
    print(db_e is False)

    if not db_e:
        # 验证密码
        new_pwd = isPassWord(pwd, pwd2)
        print(f'加密后：{new_pwd}')
        u = User(email=email, password=new_pwd, username=faker.name())
        db.session.add(u)
        db.session.commit()
        # 数据入库
        return {'message': '注册成功'}
    return {'message': '已经存在'}


# 登录接口
@user_dp.route('/login', methods=['POST'])
def login():
    #  测试中，指定账号登录
    email = request.get_json().get('email')
    pwd = request.get_json().get('pwd')
    print('前端发来的：',email, pwd)

    new_pwd = isPassWord(pwd, pwd)    # 加密密码
    # 查询用户
    u = User(email=email, password=new_pwd, username=faker.name())
    print(f'用户{u}, 密码{new_pwd}')
    if email == u.email and new_pwd == u.password:
        # 设置token
        token = generate_token(email)
        # 返回token
        return {'username': u.email, 'token': token}
    return {'message': '登录失败'}


# 令牌函数
def generate_token(user_id):
    header = {'alg': 'HS256'}
    payload = {
        'user_id': user_id,
    }
    s = os.getenv('SECRET_KEY')
    # token是一个二进制的形式，需要使用decode()进行解码
    t = jwt.encode(header, payload, s)
    return t.decode()


# 判断用户
def isPassWord(pwd,pwd2):
    if pwd == pwd2:
        # 进行加密,默认128个字符，截取64个字符
        new_pwd = blake2b(str(pwd).encode('utf-8')).hexdigest()[0:128:2]
        return new_pwd
    return False


if __name__ == '__main__':
    p = isPassWord(123,123)
    print(p)


