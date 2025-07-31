from celery import shared_task
from datetime import timedelta, datetime
from .models import DiscountPercentage
from django.utils import timezone
import pytz




@shared_task
def remove_expires_codes():
    three_days = timezone.now() - timedelta(days=3)  # استفاده از timezone.now()
    expires_codes = DiscountPercentage.objects.filter(valid_to__lt=three_days, active=True)  # اصلاح شرط فیلتر
    count = expires_codes.delete()
    return f'{count[0]} code(s) deleted!' if count[0] else 'No expired codes found.'  # بررسی مقدار
