from socket import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# 邮件服务器地址和端口
mailServer = '127.0.0.1'
mailPort = 8032

# 收件人邮箱地址
rcpt = '3296416743@qq.com'

# 构造邮件内容
msg = MIMEMultipart()
msg['From'] = 'sender@example.com'
msg['To'] = rcpt
msg['Subject'] = 'Python SMTP 测试邮件'

# 添加邮件正文
body = "这是一封通过自建 SMTP 中继服务器发送的测试邮件，包含图片附件。"
msg.attach(MIMEText(body, 'plain'))

# 添加图片附件
with open('test.jpg', 'rb') as f:
    img_data = f.read()
img = MIMEImage(img_data)
img.add_header('Content-Disposition', 'attachment', filename='test.jpg')
msg.attach(img)

# 创建 TCP 套接字并连接到邮件服务器
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))

# 接收服务器响应
recv = clientSocket.recv(1024).decode()
print("服务器响应:", recv)
if recv[:3] != '220':
    print("220 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送 HELO 命令
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print("HELO 响应:", recv1)
if recv1[:3] != '250':
    print("250 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送 MAIL FROM 命令
mailFromCommand = f'MAIL FROM:<3296416743@qq.com>\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print("MAIL FROM 响应:", recv2)
if recv2[:3] != '250':
    print("250 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送 RCPT TO 命令
rcptToCommand = f'RCPT TO:<{rcpt}>\r\n'
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print("RCPT TO 响应:", recv3)
if recv3[:3] != '250':
    print("250 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送 DATA 命令
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print("DATA 响应:", recv4)
if recv4[:3] != '354':
    print("354 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送邮件内容
email_content = msg.as_string() + "\r\n.\r\n"
clientSocket.send(email_content.encode())
recv5 = clientSocket.recv(1024).decode()
print("邮件发送响应:", recv5)
if recv5[:3] != '250':
    print("250 响应未收到，连接失败。")
    clientSocket.close()
    exit()

# 发送 QUIT 命令
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print("QUIT 响应:", recv6)

# 关闭连接
clientSocket.close()
print("邮件发送成功")


