from email.message import EmailMessage
import smtplib
from config import settings
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

def get_email_message(code: str, addressee: str):
            email = EmailMessage()
            email["Subject"] = "Code Verification"
            email["From"] = settings.SMTP_USER
            email["To"] = addressee

            email.set_content(
                'div'
                f'<h>Your code {code}</h>'
                '/div',
                subtype='html'
            )
            return email

@celery.task
def send_email_code(email: str, code: str):
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                        email = get_email_message(code=code, addressee=email)
                        server.send_message(email)

# def asdf():
#         send_email_code.delay(email= "dd",code= "q324rw3")