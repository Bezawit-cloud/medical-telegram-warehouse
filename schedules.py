from dagster import schedule
from pipeline import telegram_pipeline

@schedule(cron_schedule="0 0 * * *", job=telegram_pipeline, execution_timezone="UTC")
def daily_telegram_pipeline_schedule():
    return {}

from dagster import hook

@hook
def notify_on_failure(context, _):
    print(f"Pipeline failed! {context.failure_event.message}")
