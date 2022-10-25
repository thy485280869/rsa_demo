# -*- coding: UTF-8 -*-
# ! /usr/bin/env python
import json
from flask import Flask, render_template, request
from flask_cors import CORS
from rsa_pycryptodome import RsaTest as Rsa_Pycryptodome_Test
from rsa_cryptography import RsaTest as Rsa_Cryptography_Test


rsa_pycryptodome = Rsa_Pycryptodome_Test(new_RSA=False, key_size=2048)
rsa_cryptography = Rsa_Cryptography_Test(new_RSA=False, key_size=2048)

app=Flask(__name__, template_folder="templates")
CORS(app, supports_credentials=True)

# 模拟数据库 保存注册用户数据
users_database = []

@app.route("/login")
def login():
    return render_template('index.html')

@app.route("/rsa_register", methods=['POST'])
def rsa_register():
    data = request.form
    _content = data.get('_content', None)
    if _content is not None:
        try:
            print("注册加密结果：", _content)
            _content = rsa_pycryptodome.dec(_content)
            print("rsa解密结果：", _content)
            _content = json.loads(_content)
            print("反序列化结果：", _content)
            if getattr(_content, "uname", None) is not None or getattr(_content, "passwd", None) is not None:
                return json.dumps({"success": False, "data": "注册失败", "error": "缺少必要参数"})
            for user in users_database:
                if user['uname'] == _content['uname']:
                    return json.dumps({"success": False, "data": "注册失败", "error": "用户名已存在"})
            users_database.append(_content)
            return json.dumps({"success": True, "data": "注册成功", "error": ""})
        except BaseException as e:
            return json.dumps({"success": False, "data": "注册失败", "error": e})
    else:
        return json.dumps({"success": False, "data": "注册失败", "error": "缺少必要参数"})
    pass

@app.route("/rsa_login", methods=['POST'])
def rsa_login():
    data = request.form
    _content = data.get('_content', None)
    if _content is not None:
        try:
            print("登录加密结果：", _content)
            _content = rsa_pycryptodome.dec(_content)
            print("rsa解密结果：", _content)
            _content = json.loads(_content)
            print("反序列化结果：", _content)
            for user in users_database:
                if user['uname'] == _content['uname']:
                    if user['passwd'] == _content['passwd']:
                        return json.dumps({"success": True, "data": "解密成功,密码正确", "error": ""})
                    else:
                        return json.dumps({"success": True, "data": "解密成功,密码错误", "error": ""})
            return json.dumps({"success": True, "data": "解密成功，未找到此用户", "error": ""})
        except BaseException as e:
            return json.dumps({"success": False, "data": "解密失败", "error": e})
    else:
        return json.dumps({"success": False, "data": "解密失败", "error": "缺少必要参数"})
    pass

@app.route("/public_key", methods=['GET'])
def get_public_key():
    res = {
        "public_key": rsa_pycryptodome.get_public_key(),
    }
    return json.dumps(res)


# 测试
@app.route("/test_login")
def login_test():
    return render_template('index_test.html')

@app.route("/test_rsa_register", methods=['POST'])
def test_rsa_register():
    data = request.form
    _content = data.get('_content', None)
    if _content is not None:
        try:
            print("注册加密结果：", _content)
            _content = rsa_cryptography.dec(_content)
            print("rsa解密结果：", _content)
            _content = json.loads(_content)
            print("反序列化结果：", _content)
            if getattr(_content, "uname", None) is not None or getattr(_content, "passwd", None) is not None:
                return json.dumps({"success": False, "data": "注册失败", "error": "缺少必要参数"})
            for user in users_database:
                if user['uname'] == _content['uname']:
                    return json.dumps({"success": False, "data": "注册失败", "error": "用户名已存在"})
            users_database.append(_content)
            return json.dumps({"success": True, "data": "注册成功", "error": ""})
        except BaseException as e:
            return json.dumps({"success": False, "data": "注册失败", "error": e})
    else:
        return json.dumps({"success": False, "data": "注册失败", "error": "缺少必要参数"})

@app.route("/test_rsa_login", methods=['POST'])
def test_rsa_login():
    data = request.form
    _content = data.get('_content', None)
    if _content is not None:
        try:
            print("登录加密结果：", _content)
            _content = rsa_cryptography.dec(_content)
            print("rsa解密结果：", _content)
            _content = json.loads(_content)
            print("反序列化结果：",_content)
            for user in users_database:
                if user['uname'] == _content['uname']:
                    if user['passwd'] == _content['passwd']:
                        return json.dumps({"success": True, "data": "解密成功,密码正确", "error": ""})
                    else:
                        return json.dumps({"success": True, "data": "解密成功,密码错误", "error": ""})
            return json.dumps({"success": True, "data": "解密成功，未找到此用户", "error": ""})
        except BaseException as e:
            return json.dumps({"success": False, "data": "解密失败", "error": e})
    else:
        return json.dumps({"success": False, "data":"解密失败", "error":"缺少必要参数"})

@app.route("/test_public_key", methods=['GET'])
def get_test_public_key():
    res = {
        "public_key": rsa_cryptography.get_public_key()
    }
    return json.dumps(res)

if __name__ == "__main__":
    # 启动服务后访问 localhost:5000/login即可
    app.run(port=5000)

    # test
    # message = "This is a plain text.飒飒法吃撒爱睡觉的顶顶顶顶顶顶顶顶顶顶的饭卡vv"
    # a = rsa_cryptography.enc(message)
    # print(a)
    # b = rsa_cryptography.dec(a)
    # print(b)
