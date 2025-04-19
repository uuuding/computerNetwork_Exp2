import time
from socket import *
import threading  # 新增：导入线程模块

# 准备服务器端socket （按需补充）
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000  # 设置服务器端口号
serverSocket.bind(('', serverPort))  # 绑定服务器地址和端口
serverSocket.listen(10)  # 监听连接，允许最多10个连接等待


# 定义处理客户端请求的函数（用于多线程）
def handle_client(connectionSocket, addr):
    try:
        time.sleep(1)  # 模拟服务端处理时间为1秒
        message = connectionSocket.recv(1024).decode()  # 接收客户端发送的消息
        filename = message.split()[1]
        f = open(filename[1:])
        output_data = f.read()  # 读取文件内容
        # 通过socket发送HTTP Head
        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "Content-Type: text/html\r\n"
        response_header += f"Content-Length: {len(output_data.encode())}\r\n"
        response_header += "\r\n"
        # 发送响应
        connectionSocket.send(response_header.encode())  # 发送HTTP响应头
        connectionSocket.send(output_data.encode())  # 发送HTML正文
        connectionSocket.close()
    except IOError:
        # 发送未找到文件的相应信息(可自定义)
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head><body><h1>404 Not Found</h1></body></html>".encode())
        # 关闭客户端socket
        connectionSocket.close()


try:
    while True:
        # 建立连接
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # 接受客户端连接
        # 每接收到一个连接，就创建一个新线程去处理
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()  # 启动线程处理客户端请求
except KeyboardInterrupt:
    # 捕获 Ctrl+C 信号，关闭服务器
    print("\nServer is shutting down...")
finally:
    # 确保服务器 socket 被关闭
    serverSocket.close()
    print("Server socket closed.")
