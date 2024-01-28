from django.core.mail import send_mail

from goodreads.celery import app


@app.task()
def send_email(subject, message, recipient_list):
    send_email(
        subject,
        message,
        'vokhidov.alibek.ru@gmail.com',
        recipient_list
    )