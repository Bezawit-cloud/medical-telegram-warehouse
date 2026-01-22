from dagster import job, op
import subprocess
@op
def scrape_telegram_data():
    subprocess.run(["python", "scraper.py"], check=True)
    return "Scraping Done"

@op
def load_raw_to_postgres():
    subprocess.run(["python", "load_to_postgres.py"], check=True)
    return "Data Loaded to Postgres"

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], check=True)
    return "DBT Transformations Done"

@op
def run_yolo_enrichment():
    subprocess.run(["python", "yolo_detect.py"], check=True)
    return "YOLO Enrichment Done"
@job
def telegram_pipeline():
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres()
    dbt_done = run_dbt_transformations()
    yolo = run_yolo_enrichment()
