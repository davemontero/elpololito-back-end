import smtplib, ssl

def recovery_mail(usermail):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "elpololitocl@gmail.com"  # Enter your address
    password = "7*&$*9n37M3&%^863^4"
    receiver_email = usermail  # Enter receiver address
    message = """\
    Subject: Recuperación de cuenta

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)