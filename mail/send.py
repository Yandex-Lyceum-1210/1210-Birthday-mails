import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Функция отправки сообщения с помощью SMTP
def send(mailto, subject, text, attach=None, fromname='1210 School',
         server='smtp.gmail.com:587', frommail='notifications.1210@gmail.com', pwd='D2D-HHa-7Dp-xPH'):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromname + ' <' + frommail + '>'
    part = MIMEText(text, "html")
    msg.attach(part)
    if attach:
        part = MIMEApplication(open(attach, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=attach)
        msg.attach(part)
    try:
        server = smtplib.SMTP(server)
        server.ehlo()
        server.starttls()
        server.login(frommail, pwd)
        server.sendmail(frommail, mailto, msg.as_string())
        server.quit()
        return "Сообщение успешно отправлено адресату " + mailto + "."
    except Exception as e:
        return "ОШИБКА! Не удалось отправить сообщение адресату " + mailto + ". Тип ошибки:\n" + str(e)
