import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
from PyQt5 import QtWidgets, QtGui

class EmailWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sender_label = QtWidgets.QLabel("From:", self)
        self.sender_input = QtWidgets.QLineEdit(self)
        self.recipient_label = QtWidgets.QLabel("To:", self)
        self.recipient_input = QtWidgets.QLineEdit(self)
        self.subject_label = QtWidgets.QLabel("Subject:", self)
        self.subject_input = QtWidgets.QLineEdit(self)
        self.message_label = QtWidgets.QLabel("Message:", self)
        self.message_input = QtWidgets.QTextEdit(self)
        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_email)
        
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.sender_label, 0, 0)
        layout.addWidget(self.sender_input, 0, 1)
        layout.addWidget(self.recipient_label, 1, 0)
        layout.addWidget(self.recipient_input, 1, 1)
        layout.addWidget(self.subject_label, 2, 0)
        layout.addWidget(self.subject_input, 2, 1)
        layout.addWidget(self.message_label, 3, 0)
        layout.addWidget(self.message_input, 3, 1)
        layout.addWidget(self.send_button, 4, 1)
    def send_email(self):
        smtp_server = "SMTP SERVER";
        smtp_port = 587
        username = "SMTP USER"
        password = "SMTP PASSWORD"
        attachment_path = "Attachment PATH"
        sender = self.sender_input.text()
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        part = MIMEBase('application', "octet-stream")
        with open(attachment_path, 'rb') as file:
            part.set_payload((file.read()))
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(part)

        try:
            smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login(username, password)
            smtp_obj.sendmail(sender, [recipient], msg.as_string())
            smtp_obj.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = EmailWindow()
    window.show()
    app.exec_()
