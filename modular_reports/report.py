import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO add proper logging instead of prints
# TODO env variables
# TODO MIME mixed/related/alternative + attachments and stuff

class Report:
    def __init__(self, subject: str, text_content: str, html_content: str = None, logger = logging.getLogger(__name__)) -> None:
        self.subject = subject
        self.text_content = text_content
        self.html_content = html_content
        self.logger = logger


    def send_via_smtp_ssl(self, url, port, sender, recipients, password):
        if (self.html_content): 
            message = MIMEMultipart('alternative')
            message.attach(MIMEText(self.text_content))
            message.attach(MIMEText(self.html_content, 'html'))
        else:
            message = MIMEText(self.text_content)

        message['Subject'] = self.subject
        message['From'] = sender
        message['To'] = ', '.join(recipients if isinstance(recipients, list) else [recipients])
        
        self.logger.info(f'Sending report to {url}...')
        with smtplib.SMTP_SSL(url, port) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, message.as_string())
            self.logger.info("Report has been sent!")


    def send_via_gmail(self, sender, recipients, password):
        self.send_via_smtp_ssl('smtp.gmail.com', 465, sender, recipients, password)