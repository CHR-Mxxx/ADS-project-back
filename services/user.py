from sqlalchemy.orm import Session
import schemas.user
import models.user
import schemas.captchaEmail
import hashlib
import hmac
import secrets
import string
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
MAIL_STARTTLS = os.getenv("MAIL_STARTTLS")
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS")
USE_CREDENTIALS = os.getenv("USE_CREDENTIALS")
VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")


def create_user(db: Session, user: schemas.user.UserCreate):
    db_user = models.user.UserModel(
        email=user.email,
        username=user.username,
        password=hmac.new(
            user.password.encode, user.email.encode, hashlib.sha256
        ).hexdigest(),
        phone=user.phone,
        gender=user.gender,
        birthday=user.birthday,
        description=user.description,
        created_at=user.created_at,
        expires_at=user.expires_at,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_available=user.is_available,
    )
    db.add(db_user)
    db.commit()
    return db_user


def send_email(email: str, background_tasks: BackgroundTasks):
    emailCaptcha = "".join(secrets.choice(string.digits) for _ in range(6))
    email_content = f"""
    <p>感谢您支持我的网站！
    您发送的验证码为：{emailCaptcha}
    请在网站内进行验证。
    如果不是您本人操作，请忽略此邮件。
    请勿将验证码泄露给他人
    </p>
    """
    message = MessageSchema(
        subject="验证码",
        recipients=[email],  # List of recipients, as many as you can pass
        body=email_content,
        subtype=MessageType.html,
    )
    fm = FastMail(
        config=ConnectionConfig(
            MAIL_USERNAME=MAIL_USERNAME,
            MAIL_PASSWORD=MAIL_PASSWORD,
            MAIL_FROM=MAIL_FROM,
            MAIL_PORT=MAIL_PORT,
            MAIL_SERVER=MAIL_SERVER,
            MAIL_FROM_NAME=MAIL_FROM_NAME,
            MAIL_STARTTLS=MAIL_STARTTLS,
            MAIL_SSL_TLS=MAIL_SSL_TLS,
            USE_CREDENTIALS=USE_CREDENTIALS,
            VALIDATE_CERTS=VALIDATE_CERTS,
        )
    )
    try:
        fm.send_message(message)
        # background_tasks.add_task(fm.send_message, message)
        print("邮件发送中……")
    except Exception as e:
        print(f"邮件发送异常: {e}")
    print(f"send email to {email} with captcha {emailCaptcha}")
    return {"message": f"Captcha sent to {email}"}
