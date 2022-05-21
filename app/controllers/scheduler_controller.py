from flask_apscheduler import APScheduler
from pytz import utc
from app.controllers.redis_controller import update_forecasts

# Создание объекта планировщика
scheduler = APScheduler()


@scheduler.task('interval', id='update_horoscopes', hours=1, timezone=utc)
def job_update_horoscopes():
    """
    Функция для создания interval-job, которая будет проверять обновления гороскопа каждый час
    :return:
    """
    update_forecasts()
    print('Updated forecasts')
