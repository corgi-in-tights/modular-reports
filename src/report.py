import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Report:
    def __init__(self, title: str, content: str, log: list) -> None:
        self.title = title
        self.content = content
        self.log = log


    def send_via_smtp_ssl(self, url, port, sender, recipients, password):
        message = MIMEMultipart()

        text_part = MIMEText('\n'.join(self.log))
        html_part = MIMEText(self.content, 'html')
        message.attach(text_part)
        message.attach(html_part)

        message['Subject'] = self.title
        message['From'] = sender
        message['To'] = ', '.join(recipients if isinstance(recipients, list) else [recipients])
        

        with smtplib.SMTP_SSL(url, port) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, message.as_string())
            print("Report has been sent!")


    def send_via_gmail(self, sender, recipients, password):
        self.send_via_smtp_ssl('smtp.gmail.com', 465, sender, recipients, password)