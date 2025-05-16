from fastapi_mail import ConnectionConfig
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('TEST_EMAIL_HOST_USER'),
    MAIL_PASSWORD=os.getenv('TEST_EMAIL_HOST_PASSWORD'),
    MAIL_FROM=os.getenv('TEST_EMAIL_HOST_USER'),
    MAIL_PORT=465,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)
