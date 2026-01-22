# Ethiopian Medical Telegram Data Pipeline

This project implements a complete, production-style data pipeline for analyzing Ethiopian medical Telegram channels. The pipeline scrapes messages and images, transforms raw data into a structured data warehouse, enriches images using computer vision, exposes analytics through a REST API, and orchestrates the entire workflow using Dagster.

---

## What This Project Does

The pipeline performs five tightly integrated tasks:

• Scrapes messages and images from public Ethiopian medical Telegram channels  
• Stores raw data in a structured data lake (JSON + images)  
• Transforms raw data into a clean PostgreSQL data warehouse using dbt  
• Enriches image data using YOLO object detection  
• Exposes analytical insights via a FastAPI service  
• Automates everything using Dagster orchestration  

This ensures the data is **reliable, testable, observable, and production-ready**.

---

## Data Sources

Public Telegram channels related to Ethiopian medical businesses, including:

- Chemed  
- Lobelia Cosmetics  
- Tikvah Pharma  
- Additional channels from https://et.tgstat.com/medicine  

---

## Pipeline Architecture

Telegram → Raw Data Lake → PostgreSQL (Raw)
→ dbt Staging → dbt Star Schema
→ YOLO Image Enrichment
→ Analytical API (FastAPI)
→ Orchestrated with Dagster

---

## Repository Structure

api/ FastAPI analytical API
data/raw/ Raw JSON files and images
logs/ Scraping and pipeline logs
models/ dbt staging and mart models
src/ Scraper and YOLO scripts
tests/ Custom dbt data tests
pipeline.py Dagster pipeline definition

---

## Task Summary

### Task 1 – Data Scraping & Collection
- Extract message ID, date, text, views, forwards, and media info
- Download images per channel and message
- Store raw data as JSON partitioned by date and channel
- Log scraping activity and errors

### Task 2 – Data Modeling & Transformation
- Load raw JSON into PostgreSQL (`raw.telegram_messages`)
- Clean and standardize data using dbt staging models
- Build a **star schema**:
  - `dim_channels`
  - `dim_dates`
  - `fct_messages`
- Enforce data quality with dbt tests
- Generate dbt documentation

### Task 3 – Image Enrichment (YOLO)
- Run YOLOv8 object detection on scraped images
- Detect objects and confidence scores
- Classify images as:
  - promotional
  - product_display
  - lifestyle
  - other
- Store results in `fct_image_detections`

### Task 4 – Analytical API
FastAPI exposes warehouse insights through REST endpoints:
- Top mentioned products
- Channel activity trends
- Keyword-based message search
- Visual content statistics  
Includes Pydantic validation and OpenAPI documentation.

### Task 5 – Pipeline Orchestration
- Dagster coordinates the entire workflow
- Ensures correct execution order
- Supports scheduling, logging, monitoring, and failure alerts

---

## How to Run

```bash
# Scrape Telegram data
python src/scraper.py

# Load raw data to PostgreSQL
python src/load_raw.py

# Run dbt transformations and tests
dbt run
dbt test

# Run YOLO image detection
python src/yolo_detect.py

# Start API server
uvicorn api.main:app --reload

# Launch Dagster
dagster dev -f pipeline.py



