import timeit
from rsa_pycryptodome import RsaTest as Rsa_Pycryptodome_Test
from rsa_cryptography import RsaTest as Rsa_Cryptography_Test

rsa1024_pycryptodome = Rsa_Pycryptodome_Test(new_RSA=False, key_size=1024)
def test_rsa1024_pycryptodome(data):
    temp = rsa1024_pycryptodome.enc(data)
    if data != rsa1024_pycryptodome.dec(temp):
        raise ValueError("错误")
    pass

rsa2048_pycryptodome = Rsa_Pycryptodome_Test(new_RSA=False, key_size=2048)
def test_rsa2048_pycryptodome(data):
    temp = rsa2048_pycryptodome.enc(data)
    if data != rsa2048_pycryptodome.dec(temp):
        raise ValueError("错误")
    pass

rsa1024_cryptography = Rsa_Cryptography_Test(new_RSA=False, key_size=1024)
def test_rsa1024_cryptography(data):
    temp = rsa1024_cryptography.enc(data)
    if data != rsa1024_cryptography.dec(temp):
        raise ValueError("错误")
    pass

rsa2048_cryptography = Rsa_Cryptography_Test(new_RSA=False, key_size=2048)
def test_rsa2048_cryptography(data):
    temp = rsa2048_cryptography.enc(data)
    if data != rsa2048_cryptography.dec(temp):
        raise ValueError("错误")
    pass

def test_func(func_name, args, count=1000):
    """
    :param func_name: 测试函数名
    :param args: 传入参数
    :param count: 测试次数
    :return:
    """
    res = timeit.timeit(
        stmt=f"{func_name}(\'{args}\')",
        setup=f"from __main__ import {func_name}",
        number=count
    )


    return res

if __name__ == "__main__":
    # 基于同模式下，不同密钥长度对加解密性能的影响
    test_data = '123asf3jvjdfb9d;看发送框反馈【的披萨盘{dpsfldsf'
    for func_name in ["test_rsa1024_pycryptodome", "test_rsa2048_pycryptodome", "test_rsa1024_cryptography", "test_rsa2048_cryptography"]:
        res = test_func(func_name, test_data)
        print(func_name, res)
