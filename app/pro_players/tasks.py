import logging
from celery import shared_task
from django.core.mail import send_mail


logger = logging.getLogger(__name__)

@shared_task
def send_email_notification(message, subject, sender_email, to):
    try:
        send_mail(subject, message, sender_email, to, fail_silently=False)
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise