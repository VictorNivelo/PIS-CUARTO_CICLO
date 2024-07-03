import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'victor.nivelo0909@gmail.com'
smtp_password = 'a'

sender = 'victor.nivelo0909@gmail.com'
receiver = 'victor.david0909@gmail.com'
subject = 'Prueba de correo desde Python'
body = 'Hola,\n\nEste es un correo de prueba enviado desde Python.'

msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = formataddr(('Django App', sender))
msg['To'] = receiver

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(sender, [receiver], msg.as_string())
    print('Correo enviado correctamente')
except Exception as e:
    print(f'Error al enviar correo: {str(e)}')
finally:
    server.quit()
