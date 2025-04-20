import socket
import smtplib
from email import message_from_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class SMTPServer:
    def __init__(self, host='127.0.0.1', port=8032):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"SMTP server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        print("New connection from", client_socket.getpeername())
        client_socket.send("220 SMTP Server Ready\r\n".encode())

        data_buffer = ""
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            data_buffer += data
            print("Received data:", data)  # 添加调试信息

            # 检查是否收到完整的邮件内容
            if data_buffer.endswith("\r\n.\r\n"):
                # 处理完整的邮件内容
                self.forward_email(data_buffer)
                client_socket.send("250 OK\r\n".encode())
                data_buffer = ""
            else:
                # 处理命令
                lines = data_buffer.split("\r\n")
                data_buffer = lines[-1] if lines else ""
                for line in lines[:-1]:
                    if line.startswith("HELO"):
                        client_socket.send("250 Hello\r\n".encode())
                    elif line.startswith("MAIL FROM:"):
                        client_socket.send("250 OK\r\n".encode())
                    elif line.startswith("RCPT TO:"):
                        client_socket.send("250 OK\r\n".encode())
                    elif line == "DATA":
                        client_socket.send("354 End data with <CR><LF>.<CR><LF>\r\n".encode())
                    elif line == "QUIT":
                        client_socket.send("221 Bye\r\n".encode())
                        return
                    else:
                        print("Unknown command:", line)  # 添加调试信息
                        client_socket.send("500 Error\r\n".encode())

        client_socket.close()

    def forward_email(self, message):
        # 使用 email 库解析邮件
        msg = message_from_string(message)
        from_addr = msg['From']
        to_addr = msg['To']
        subject = msg['Subject']

        # 构造新的邮件
        new_msg = MIMEMultipart()
        new_msg['From'] = '1718973225@qq.com'
        new_msg['To'] = to_addr
        new_msg['Subject'] = subject

        # 添加邮件正文和附件
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    new_msg.attach(MIMEText(body, 'plain'))
                elif content_type.startswith('image/'):
                    payload = part.get_payload(decode=True)
                    image = MIMEImage(payload)
                    image.add_header('Content-Disposition', 'attachment', filename=part.get_filename())
                    new_msg.attach(image)
        else:
            body = msg.get_payload(decode=True).decode()
            new_msg.attach(MIMEText(body, 'plain'))


        self.send_email('smtp.qq.com', 465, '1718973225@qq.com', 'ousrgihwzysebacf', to_addr, subject,
                        new_msg.as_string())

    def send_email(self, smtp_host, smtp_port, sender, password, recipient, subject, message):
        try:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(sender, password)
                server.sendmail(sender, recipient, message)
                print("Email sent successfully.")
        except Exception as e:
            return

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.handle_client(client_socket)

if __name__ == "__main__":
    server = SMTPServer()
    server.start()