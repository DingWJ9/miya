import socket
import random
import unittest
sk = socket.socket()
#创建实例
sk = socket.socket()
ip_port =("127.0.0.1",8888)
#绑定监听
sk.bind(ip_port)
#最大连接数
sk.listen(5)
while True:
    #提示信息
    print("正在进行等待接收数据。。。")
    #接收数据
    conn,address = sk.accept()
    #定义信息
    msg = "连接成功!"
    conn.send(msg.encode())
    # 不断接收客户端发来的消息
    while True:
        # 接收客户端消息
        data = conn.recv(1024)
        print(data.decode())
        if data ==b'exit':
            break
        # 处理客户端消息
        conn.send(str(random.randint(1,10000)).encode())
        # 发送随机数信息
        #主动关闭连接
    conn.close()