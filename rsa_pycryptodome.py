import base64
import time

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

# 基于pycryptodome库的RSA算法：底层用python实现，性能低
class RsaTest(object):
    def __init__(self, new_RSA=False, key_size=2048):
        """
        :param new_RSA: 是否重新生成公钥私钥
        :param key_size: 密钥长度。推荐2048长度
        """
        self.public_key_file_path = "public_key.pem"
        self.private_key_file_path = "private_key.pem"

        if new_RSA:
            random_generator = Random.new().read
            rsa = RSA.generate(key_size, random_generator)
            # 生成私钥、公钥
            private_key = rsa.exportKey()
            public_key = rsa.publickey().exportKey()
            # 将公钥私钥保存到文件中
            with open(self.private_key_file_path, 'wb') as f:
                f.write(private_key)
            with open(self.public_key_file_path, 'wb') as f:
                f.write(public_key)

        # 从文件中读取公钥私钥值  预加载
        with open(self.private_key_file_path, 'r') as f:
            self.private_key = f.read()
        with open(self.public_key_file_path, 'r') as f:
            self.public_key = f.read()

        # 预加载加密相关参数 提高性能
        self.public_key_cipher_obj = PKCS1_v1_5.new(RSA.importKey(self.public_key))
        # 预加载解密相关参数 提高性能
        self.private_key_cipher_obj = PKCS1_v1_5.new(RSA.importKey(self.private_key))
        self.random_generator = Random.new().read
        pass

    def get_public_key(self):
        return self.public_key

    def enc(self, data):
        cipher_text = (self.public_key_cipher_obj.encrypt(data.encode('utf-8')))
        # print('加密返回值: ', cipher_text)
        return base64.b64encode(cipher_text).decode('utf-8')
        pass

    def dec(self, data):
        data = base64.b64decode(data.encode('utf-8'))
        start = time.perf_counter()
        plain_text = self.private_key_cipher_obj.decrypt(data, self.random_generator)
        # print('解密返回值: ', plain_text.decode('utf-8'))
        print(f"pycryptodome解密耗时：{time.perf_counter()-start}s")
        return plain_text.decode('utf-8')
        pass


if __name__ == "__main__":
    r = RsaTest()
    data = "发飞洒飞洒发saksafk3921412"
    print("原始值：", data)
    edata = r.enc(data)
    print("加密结果：",edata)
    res = r.dec(edata)
    print("解密结果：",res)
    pass
