from django.db import migrations
from django_celery_beat.models import PeriodicTask, \
    CrontabSchedule


def create_periodic_tasks(apps, schema_editor):
    """
    Create periodic tasks
    :param apps
    :param schema_editor
    :return: None
    """
    # --------Send notification of the results of daily update status------
    schedule_weekly_10, created = CrontabSchedule.objects.get_or_create(
        day_of_week="2,3,4,5,6",
        hour=10
    )
    schedule_weekly_12, created = CrontabSchedule.objects.get_or_create(
        day_of_week="2,3,4,5,6",
        hour=12
    )
    schedule_weekly_14, created = CrontabSchedule.objects.get_or_create(
        day_of_week="2,3,4,5,6",
        hour=14
    )
    schedule_weekly_monday, created = CrontabSchedule.objects.get_or_create(
        day_of_week=1,
        hour=10
    )
    PeriodicTask.objects.create(
        crontab=schedule_weekly_10,
        name='Update movies weekly',
        task='tasks.tasks.update_movies_weekly_task')

    PeriodicTask.objects.create(
        crontab=schedule_weekly_12,
        name='Update series weekly',
        task='tasks.tasks.update_series_weekly_task')

    PeriodicTask.objects.create(
        crontab=schedule_weekly_14,
        name='Update games weekly',
        task='tasks.tasks.update_games_weekly_task')

    PeriodicTask.objects.create(
            crontab=schedule_weekly_monday,
            name='Update all weekly',
            task='tasks.tasks.review_empty_fields_task')


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_periodic_tasks),
    ]
