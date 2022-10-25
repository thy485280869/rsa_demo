import time

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# 基于cryptography库的RSA算法：底层用C\C++实现，性能比pycryptodome高，使用timeit进行性能测试能达到微秒级别
class RsaTest(object):
    def __init__(self, new_RSA=False, key_size=2048):
        self.public_key_file_path = "public_key.pem"
        self.private_key_file_path = "private_key.pem"

        if new_RSA:
            # 生成公钥私钥
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
            # 将公钥私钥以pem文件格式保存
            pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(self.private_key_file_path, 'wb') as f:
                f.write(pem)
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(self.public_key_file_path, 'wb') as f:
                f.write(pem)
        else:
            # 加载私秘钥对象
            with open(self.private_key_file_path, 'rb') as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
                self.public_key = self.private_key.public_key()

        # 预加载公钥内容
        with open(self.public_key_file_path, 'r') as f:
            self.public_key_text = f.read()

    def get_public_key(self):
        return self.public_key_text

    def enc(self, message):
        message = message.encode('utf-8')
        public_key = self.public_key
        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted = base64.b64encode(encrypted)
        return encrypted.decode('utf-8')

    def dec(self, encrypted_data):
        """
        前端jsrsasign包生成的密文为一串16进制数，用base64编码后才发生给后端，所以后端解密前需要base64解密，保持一致性
        rsa解密算法和填充方式也得与前端保持一致
        :param encrypted_data:
        :return:
        """
        encrypted_data = base64.b64decode(encrypted_data)
        start = time.perf_counter()
        original_message = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"cryptography解密耗时：{time.perf_counter()-start}s")
        return original_message.decode('utf-8')

if __name__ == "__main__":
    r = RsaTest()
    data = "发飞洒飞洒发saksafk3921412"
    print("原始值：", data)
    edata = r.enc(data)
    print("加密结果：",edata)
    res = r.dec(edata)
    print("解密结果：",res)
    pass
