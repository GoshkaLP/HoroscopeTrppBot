from flask_apscheduler import APScheduler
from datetime import timezone
from app.controllers.redis_controller import update_forecasts

# Создание объекта планировщика
scheduler = APScheduler()


@scheduler.task('cron', id='update_horoscopes', hour=22, timezone=timezone.utc)
def job_update_horoscopes():
    """
    Функция для создания cron-job, которая будет обновлять гороскопы каждые сутки
    :return:
    """
    update_forecasts()
    print('Updated forecasts')
