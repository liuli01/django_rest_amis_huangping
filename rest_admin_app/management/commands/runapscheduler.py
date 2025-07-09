import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from rest_admin_app.scheduler import my_job,fetch_device_data,clean_device_data,history_trend_clean_all

logger = logging.getLogger(__name__)



# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  清理超过 max_age 秒的任务执行记录，防止 job execution 表膨胀
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age=max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # scheduler.add_job(
    #   my_job,
    #   trigger=CronTrigger(second="*/10"),  # Every 10 seconds
    #   id="my_job",  # The `id` assigned to each job MUST be unique
    #   max_instances=1,
    #   replace_existing=True,
    # )
    # logger.info("Added job 'my_job'.")

    scheduler.add_job(
      fetch_device_data,
      trigger=IntervalTrigger(minutes=10),  # Every 10 seconds
      id="fetch_device_data",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'fetch_device_data'.")




    scheduler.add_job(
            clean_device_data,
            trigger=IntervalTrigger(minutes=10),
            id="clean_data_job",
            name="每10分钟清洗一次数据",
            replace_existing=True,
        )
    
     # 立刻执行一次
    logger.info("启动时立即执行 history_trend_clean_all")
    history_trend_clean_all()

    scheduler.add_job(
            history_trend_clean_all,
            trigger=CronTrigger(hour="0", minute="0"),  # 每天午夜
            id="history_trend_clean_all",
            name="每天午夜清洗一次数据",
            replace_existing=True,
        )
    


    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("开始调度...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("停止调到中...")
      scheduler.shutdown()
      logger.info("调度关闭成功!")


        
