from socket import *
import random

# 创建一个UDP套接字
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", 12000))  # 绑定端口 12000

print("UDP服务器已启动，监听端口 12000...")

while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()

    # 模拟30%的数据包丢失
    if rand < 4:
        print("模拟丢包：未响应客户端")
        continue

    serverSocket.sendto(message, address)
    print(f"已响应客户端 {address}：{message.decode()}")
