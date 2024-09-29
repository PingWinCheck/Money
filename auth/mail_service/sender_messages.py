from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from uuid import UUID

from pydantic import EmailStr

from settings import settings
from auth.mail_service.utils import generate_token
from auth.redis import redis_client


def send_message_verification_mail(to: EmailStr, user_id: UUID):
    message = MIMEMultipart()
    message['From'] = settings.smtp_login
    message['To'] = to
    message['Subject'] = 'Подтвержение регистрации на сайте'
    token = generate_token()
    redis_client.set(name=token, value=str(user_id), ex=60 * 60)

    url = f'http://localhost:8000/auth/confirm-mail/{token}'
    body = f"""Подтвердите регистрацию перейдя по ссылке {url}
    Если вы не совершали никаких действии, просто проигнорируйте это сообщение
    """
    message.attach(MIMEText(body))
    with SMTP(host='smtp.mail.ru', port=587) as server:
        server.starttls()
        server.login(user=settings.smtp_login, password=settings.smtp_pass)
        server.send_message(message)







