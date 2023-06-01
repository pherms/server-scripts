import email, smtplib
import os
import modules as mods

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(smtp_server,recipient,subject,message_text,logfile=None):
    port = 25
    sender_email = "no_reply@pascalherms.nl"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    if not logfile is None:
        filename = logfile.name

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

def sendMailFailedBackup(hostname,message):
    config = mods.readConfig()
    mailServer = config["mailserver"]
    recipient = config["mailRecipient"]

    subject = "Backup van server {} gefaald".format(hostname)

    sendMail(mailServer,recipient,subject,message)

def sendMailFailedCopyToServer(hostname,message):
    config = mods.readConfig()
    mailServer = config["mailserver"]
    recipient = config["mailRecipient"]

    subject = "Kopieren van files van server {} is gefaald".format(hostname)

    sendMail(mailServer,recipient,subject,message)

def sendMailFailedCleanup(hostname,message):
    config = mods.readConfig()
    mailServer = config["mailserver"]
    recipient = config["mailRecipient"]

    subject = "Cleanup van server {} is gefaald".format(hostname)

    sendMail(mailServer,recipient,subject,message)