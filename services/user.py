from sqlalchemy.orm import Session
import schemas.user
import models.user
import hashlib
import hmac
import secrets
import string
from fastapi import BackgroundTasks
import smtplib
import os
import email
from dotenv import load_dotenv
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import redis
from datetime import datetime, timedelta
from schemas.user import UserCreate, UserPublic
from services.mydb import get_db

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


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def create_user(db: Session, user: schemas.user.UserCreate):
    db_user = models.user.UserModel(
        email=user.email,
        username=user.username,
        password=hmac.new(
            user.password.encode(), user.email.encode(), hashlib.sha256
        ).hexdigest(),
        phone=user.phone,
        gender=user.gender,
        birthday=user.birthday,
        description=user.description,
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=30),
        updated_at=datetime.now(),
        is_active=(
            True  # 是否为激活状态，若不是激活状态则无法保持登录状态，需重新登录
        ),
        is_superuser=False,  # 是否为超级用户
        is_available=True,
    )
    db.add(db_user)
    db.commit()
    return db_user


def send_email(email: str, background_tasks: BackgroundTasks):
    emailCaptcha = "".join(secrets.choice(string.digits) for _ in range(6))
    email_content = f"""
    感谢您支持我的网站！
    您发送的验证码为：{emailCaptcha}
    请在网站内进行验证。
    如果不是您本人操作，请忽略此邮件。
    请勿将验证码泄露给他人。
    """
    msg = MIMEText(email_content, "plain", "utf-8")
    msg["From"] = _format_addr(f"{MAIL_FROM_NAME} <{MAIL_FROM}>")
    msg["To"] = email
    msg["Subject"] = Header("来自PhiHelper网站的验证码", "utf-8").encode()

    smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtp.set_debuglevel(2)
    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
    try:
        smtp.sendmail(MAIL_FROM, [email], msg.as_string())
        print("邮件发送中……")
        print(f"send email to {email} with captcha {emailCaptcha}")
        smtp.quit()
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.setex(email, 300, emailCaptcha)  # 5分钟过期
        return {
            "message": f"Captcha sent to {email} successfully! :)",
            "status": "success",
        }
    except Exception as e:
        print(f"邮件发送异常: {e}")
        return {
            "message": "Failed to send captcha to your email. :(",
            "status": "error",
        }


def register_user(db: Session, user: UserPublic, inputCaptcha: str):
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    stored_captcha = r.get(user.email)
    # if stored_captcha is None:
    #     return {"status": "error", "message": "验证码已过期或不存在。"}

    # if stored_captcha != inputCaptcha:
    #     return {"status": "error", "message": "此验证码错误或为过期验证码。"}

    new_user = create_user(db, user)
    print(new_user)
    return {"status": "success", "message": "User registered successfully."}
