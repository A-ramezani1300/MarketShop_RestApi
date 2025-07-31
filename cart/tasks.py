from celery import shared_task
from datetime import timedelta, datetime
from .models import CartItem
from django.utils.timezone import now
import pytz



# @shared_task()
# def remove_expires_cart_items():
#     one_week_ago = now() - timedelta(days=7)
#     expires_items = CartItem.objects.filter(added_at__lt=one_week_ago, status='pending')
#     expires_items.delete()



@shared_task()
def remove_expires_cart_items():
    one_week_ago = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
    expires_items = CartItem.objects.filter(added_to_cart__lt=one_week_ago, status='pending')
    count = expires_items.delete()
    return f'{count[0]} items is deleted!'

