import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jarbas.settings')

app = Celery('jarbas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from django.core import management

    @app.task(ignore_result=True)
    def searchvector():
        print('Running searchvector...')
        management.call_command('searchvector')
        print('Searchvector is done')

    if settings.SCHEDULE_SEARCHVECTOR:
        sender.add_periodic_task(
            crontab(
                minute=settings.SCHEDULE_SEARCHVECTOR_CRON_MINUTE,
                hour=settings.SCHEDULE_SEARCHVECTOR_CRON_HOUR,
                day_of_week=settings.SCHEDULE_SEARCHVECTOR_CRON_DAY_OF_WEEK,
                day_of_month=settings.SCHEDULE_SEARCHVECTOR_CRON_DAY_OF_MONTH,
                month_of_year=settings.SCHEDULE_SEARCHVECTOR_CRON_MONTH_OF_YEAR,
            ),
            searchvector.s(),
        )
