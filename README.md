# Ethiopian Medical Telegram Analytics Pipeline

> End-to-end pipeline to scrape messages and images from Ethiopian medical Telegram channels, transform them into a clean data warehouse, enrich images with YOLO object detection, serve analytics via a REST API, and orchestrate all tasks with Dagster.

This project implements a complete workflow: 

1. **Data Scraping:** Extract messages and images from channels like [Chemed](https://t.me/lobelia4cosmetics) and [Tikvah Pharma](https://t.me/tikvahpharma). For each message, capture `message_id`, `date`, `text_content`, `view_count`, `forward_count`, and media info. Images are downloaded to `data/raw/images/{channel_name}/{message_id}.jpg` and messages saved as JSON in `data/raw/telegram_messages/YYYY-MM-DD/{channel_name}.json`. All scraping activities and errors are logged in `logs/`.

2. **Data Transformation:** Load raw JSON into PostgreSQL (`raw.telegram_messages`). Clean and standardize data with dbt staging models, casting types, renaming columns, filtering invalid records, and adding calculated fields (`message_length`, `has_image`). Transform into a **star schema**: `dim_channels` (channel info), `dim_dates` (date dimension), `fct_messages` (fact table with message metrics). dbt tests include unique, not_null, relationships, plus custom tests (`assert_no_future_messages`, `assert_positive_views`). Documentation is generated via `dbt docs serve`.

3. **Data Enrichment:** Run YOLOv8 nano model on downloaded images (`src/yolo_detect.py`) to detect objects and assign classifications: `promotional` (person + product), `product_display` (product only), `lifestyle` (person only), `other` (neither). Results are saved with confidence scores and integrated into `fct_image_detections` joined with messages for analytics.

4. **Analytical API:** FastAPI exposes endpoints for business insights:
   - `/api/reports/top-products?limit=10` – Most mentioned products/terms.
   - `/api/channels/{channel_name}/activity` – Channel posting trends.
   - `/api/search/messages?query=paracetamol&limit=20` – Search messages by keyword.
   - `/api/reports/visual-content` – Statistics on image usage.  
   API uses Pydantic validation, error handling, and OpenAPI docs available at `/docs`.

5. **Pipeline Orchestration:** Dagster automates the workflow: `scrape_telegram_data → load_raw_to_postgres → run_dbt_transformations → run_yolo_enrichment`. Supports scheduling, monitoring via UI (`http://localhost:3000`), logs, and alerts for failures.

**Project Structure:**
├── api/ # FastAPI app
├── data/raw/ # JSON messages & images
├── logs/ # Scraper & pipeline logs
├── models/ # dbt staging & marts
├── src/
│ ├── scraper.py # Telegram scraper
│ └── yolo_detect.py # YOLO object detection
├── tests/ # dbt custom tests
├── pipeline.py # Dagster pipeline
├── README.md
└── requirements.txt
**Setup & Installation:**
```bash
pip install -r requirements.txt
pip install dbt-postgres
dbt init medical_warehouse
pip install dagster dagster-webserver
pip install fastapi uvicorn SQLAlchemy
Usage:
python src/scraper.py             # Run scraper
python src/load_raw.py            # Load JSON to PostgreSQL
dbt run && dbt test               # Run dbt transformations and tests
python src/yolo_detect.py         # YOLO image enrichment
uvicorn api.main:app --reload     # Start API server
dagster dev -f pipeline.py        # Run Dagster pipeline
** Insights: Compare views for promotional vs product_display posts, identify channels with most visual content, and note limitations of pre-trained YOLO models for domain-specific detection**

---




