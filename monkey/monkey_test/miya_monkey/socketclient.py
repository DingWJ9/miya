import socket
import google.protobuf
import int_pb2
client = socket.socket()
# 访问服务器端的IP和端口
# ip_port = ("127.0.0.1",8888)
ip_port =("staging-s.miyachat.com",9900)
# 连接主机
client.connect(ip_port)
# 接收主机信息
# 打印接收数据
while True:
    # 接收主机信息
    data = client.recv(1024)
    print(data.decode())
    # 输入发送的消息
    msg_input = input("请输入发送的消息：")
    #消息发送
    client.send(msg_input.encode())
    if msg_input == "exit":
        break
data = client.recv(1024)
print(data.decode())