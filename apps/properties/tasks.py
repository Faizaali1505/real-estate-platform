from celery import shared_task
from .email_alerts import check_and_send_alerts


@shared_task
def send_saved_search_alerts():
    
    check_and_send_alerts()
    return "Email alerts check complete"