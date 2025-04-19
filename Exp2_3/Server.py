import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received:", data)

            if data.startswith("HELO"):
                client_socket.send("250 Hello\r\n".encode())
            elif data.startswith("MAIL FROM:"):
                client_socket.send("250 OK\r\n".encode())
            elif data.startswith("RCPT TO:"):
                client_socket.send("250 OK\r\n".encode())
            elif data == "DATA\r\n":
                client_socket.send("354 End data with <CR><LF>.<CR><LF>\r\n".encode())
            elif data.endswith("\r\n.\r\n"):
                client_socket.send("250 OK\r\n".encode())
                self.forward_email(data)
            elif data == "QUIT\r\n":
                client_socket.send("221 Bye\r\n".encode())
                break
            else:
                client_socket.send("500 Error\r\n".encode())

        client_socket.close()

    def forward_email(self, message):
        # Extract email details from the message
        lines = message.splitlines()
        from_addr = None
        to_addr = None
        subject = None
        body = []
        for line in lines:
            if line.startswith("From:"):
                from_addr = line.split(":")[1].strip()
            elif line.startswith("To:"):
                to_addr = line.split(":")[1].strip()
                print(to_addr)
            elif line.startswith("Subject:"):
                subject = line.split(":")[1].strip()
            elif line.strip() == "":
                continue
            elif line.startswith("."):
                body.append(line[1:])
            else:
                body.append(line)

        # Send the email to QQ email
        self.send_email("smtp.qq.com", 465, "1718973225@qq.com", "ousrgihwzysebacf", to_addr, subject, "\n".join(body))

    def send_email(self, smtp_host, smtp_port, sender, password, recipient, subject, body):
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(sender, password)
                server.sendmail(sender, recipient, message.as_string())
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