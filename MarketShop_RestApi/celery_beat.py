from datetime import timedelta
from celery.schedules import crontab




CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'




CELERY_BEAT_SCHEDULE = {
    # ----------------------------------------------------
    # تسک مربوط به اپلیکیشن سبد خرید (cart)
    'remove_expires_items': {
        'task': 'cart.tasks.remove_expires_cart_items',
        'schedule': crontab(weeks=1, hour=11, minute=45), # هر هفته یک بار اجرا شود
        'args': (),
    },
    # ----------------------------------------------------
    # تسک مربوط به اپلیکیشن سفارش‌ها (orders)
    'remove_expires_code': {
        'task': 'orders.tasks.remove_expires_codes',
        'schedule': crontab(weeks=1, hour=12, minute=35), # هر هفته یک بار اجرا شود
        'args': (),
    },
}