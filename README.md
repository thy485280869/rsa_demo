**test.py文件是性能测试文件，运行后可以打印测试结果（1000次加解密结果）：**

```
test_rsa1024_pycryptodome 5.4410345(s)
test_rsa2048_pycryptodome 5.317147899999999(s)
test_rsa1024_cryptography 0.6586130000000008(s)
test_rsa2048_cryptography 0.6512908(s)

由结果可知cryptography比pycryptodome库快接近10倍，达到了微秒级别。（注意：受电脑本身性能影响，不同电脑测试结果可能有差异。）
```

**main.py是主函数，运行后启动一个http服务器**

- 本地浏览器访问http://localhost:5000/login，可测试前端jsencrypt库与后端pycryptodome库

- 本地浏览器访问http://localhost:5000/test_login，可测试前端jsrsasign库与后端cryptography库

- 基于前后端测试，也能发现cryptography比pycryptodome至少快3倍左右，下面是控制台打印结果：
  发送多次登录请求后，发现cryptography解密时间稳定在0.6ms左右，pycryptodome解密时间稳定在6ms左右，此结果与timeit中测试结果10倍性能差距相符合。

  ```
  127.0.0.1 - - [17/Sep/2022 00:22:57] "POST /rsa_register HTTP/1.1" 200 -
  pycryptodome解密耗时：0.00544179999999983s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  127.0.0.1 - - [17/Sep/2022 00:22:49] "POST /test_rsa_register HTTP/1.1" 200 -
  cryptography解密耗时：0.0018430999999999999s
  rsa解密结果： {"uname":"123","passwd":"202cb962ac59075b964b07152d234b70"}
  反序列化结果： {'uname': '123', 'passwd': '202cb962ac59075b964b07152d234b70'}
  127.0.0.1 - - [17/Sep/2022 00:23:14] "POST /rsa_login HTTP/1.1" 200 -
  pycryptodome解密耗时：0.004638899999999779s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  127.0.0.1 - - [17/Sep/2022 00:23:22] "POST /test_rsa_login HTTP/1.1" 200 -
  cryptography解密耗时：0.0015556999999972732s
  rsa解密结果： {"uname":"123","passwd":"202cb962ac59075b964b07152d234b70"}
  反序列化结果： {'uname': '123', 'passwd': '202cb962ac59075b964b07152d234b70'}
  127.0.0.1 - - [17/Sep/2022 00:27:07] "POST /test_rsa_login HTTP/1.1" 200 -
  cryptography解密耗时：0.0011340000000359396s
  rsa解密结果： {"uname":"123","passwd":"202cb962ac59075b964b07152d234b70"}
  反序列化结果： {'uname': '123', 'passwd': '202cb962ac59075b964b07152d234b70'}
  cryptography解密耗时：0.0006524000000354135s
  rsa解密结果： {"uname":"123","passwd":"202cb962ac59075b964b07152d234b70"}
  反序列化结果： {'uname': '123', 'passwd': '202cb962ac59075b964b07152d234b70'}
  127.0.0.1 - - [17/Sep/2022 00:27:11] "POST /test_rsa_login HTTP/1.1" 200 -
  127.0.0.1 - - [17/Sep/2022 00:27:14] "POST /test_rsa_login HTTP/1.1" 200 -
  cryptography解密耗时：0.0006917000000044027s
  rsa解密结果： {"uname":"123","passwd":"202cb962ac59075b964b07152d234b70"}
  反序列化结果： {'uname': '123', 'passwd': '202cb962ac59075b964b07152d234b70'}
  pycryptodome解密耗时：0.004912100000012742s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  127.0.0.1 - - [17/Sep/2022 00:27:20] "POST /rsa_login HTTP/1.1" 200 -
  127.0.0.1 - - [17/Sep/2022 00:27:22] "POST /rsa_login HTTP/1.1" 200 -
  pycryptodome解密耗时：0.00643209999998362s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  127.0.0.1 - - [17/Sep/2022 00:27:26] "POST /rsa_login HTTP/1.1" 200 -
  pycryptodome解密耗时：0.005597500000021682s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  127.0.0.1 - - [17/Sep/2022 00:27:31] "POST /rsa_login HTTP/1.1" 200 -
  pycryptodome解密耗时：0.006644300000004932s
  rsa解密结果： {"uname":"321","passwd":"caf1a3dfb505ffed0d024130f58c5cfa"}
  反序列化结果： {'uname': '321', 'passwd': 'caf1a3dfb505ffed0d024130f58c5cfa'}
  ```

  

**rsa开头的两个py文件分别是两个库的相关加解密实现。**

