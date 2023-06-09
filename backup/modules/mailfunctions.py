import email, smtplib
import os
import modules as mods

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(subject,message_text,logfile=None):
    """
    Verzend een email. Wanneer de logfile parameter niet is meegegeven, dan wordt er geen attachment aan de mail toegevoegd.

    :param str subject: het onderwerp wat moet worden meegegeven in het email bericht
    :param str message_text: de mail body text
    :param str logfile: optioneel. De logfile welke als attachment moet worden meegestuurd
    """
    config = mods.readConfig()
    sender_email = config["mailSender"]
    recipient = config["mailRecipient"]
    smtp_server = config["mailserver"]
    port = 25
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
    """
    Verzend een email wanneer de backup is gefaald. Er wordt geen attachment mee gestuurd

    :param str hostname: de hostname waarop de backup is gefaald
    :param str message: de mail body text
    """
    subject = "Backup van server {} gefaald".format(hostname)
    sendMail(subject,message)

def sendMailFailedCopyToServer(hostname,message):
    """
    Verzend een email wanneer de copy actie van de backup file naar de server is gefaald. Er wordt geen attachment mee gestuurd

    :param str hostname: de hostname waarop de copy taak is gefaald
    :param str message: de mail body text
    """
    subject = "Kopieren van files van server {} is gefaald".format(hostname)
    sendMail(subject,message)

def sendMailFailedCleanup(hostname,message):
    """
    Verzend een email wanneer de cleanup is gefaald. Er wordt geen attachment mee gestuurd

    :param str hostname: de hostname waarop de cleanup is gefaald
    :param str message: de mail body text
    """
    subject = "Cleanup van server {} is gefaald".format(hostname)
    sendMail(subject,message)