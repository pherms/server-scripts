import email, smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(smtp_server,recipient,subject,message_text,logfile):
    port = 25
    sender_email = "no_reply@pascalherms.nl"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    filename = logfile

    with open(filename, "rb") as attachement:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachement.read())
    
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.sendmail(sender_email, recipient, text)