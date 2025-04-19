import time
from socket import *

# 准备服务器端socket （按需补充）
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000  # 设置服务器端口号
serverSocket.bind(('', serverPort))  # 绑定服务器地址和端口
serverSocket.listen(1)  # 监听连接

try:
    while True:
        time.sleep(1)  # 模拟服务端处理时间为1秒
        # 建立连接
        print('Ready to serve...')
        connectionSocket, addr= serverSocket.accept() # 接受客户端连接
        try:
            message=connectionSocket.recv(1024).decode() # 接收客户端发送的消息
            filename=message.split()[1]
            f=open(filename[1:])
            output_data=f.read() # 读取文件内容
            # 通过socket发送HTTP Head
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) # 发送HTTP响应头
            connectionSocket.send(output_data.encode())
            connectionSocket.close()
        except IOError:
            # 发送未找到文件的相应信息(可自定义)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><head><body><h1>404 Not Found</h1></body></html>".encode())
            # 关闭客户端socket
            connectionSocket.close()
except KeyboardInterrupt:
    # 捕获 Ctrl+C 信号，关闭服务器
    print("\nServer is shutting down...")
finally:
    # 确保服务器 socket 被关闭
    serverSocket.close()
    print("Server socket closed.")