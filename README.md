# Medical Telegram Data Warehouse Project

This project extracts messages and images from **Telegram channels** related to Ethiopian medical businesses, stores them in a **raw data lake**, and transforms them into a clean, structured **data warehouse** using **dbt**.  
It demonstrates a full **Extract → Load → Transform (ELT)** pipeline, from raw data collection to analytics-ready tables.

---

## Task 1: Data Scraping and Collection

### Objective
Build a pipeline to extract Telegram messages and media, storing them in a raw data lake for further processing.

### Implementation
- Python script (`src/scraper.py`) uses **Telethon** to scrape messages from public Telegram channels.
- Extracted data is stored as **JSON files** in a **partitioned folder structure**:

- Images are downloaded and organized by channel and message ID:

- Logs of scraping activity, including errors and progress, are saved in `logs/`.

### Collected Data Fields
- Message ID  
- Message date  
- Message text  
- View count  
- Forward count  
- Media information (if available)  

---

## Task 2: Data Modeling and Transformation

### Objective
Transform raw, messy data into a clean, structured **data warehouse** optimized for analysis using **dbt** and a **star schema**.

### Implementation Steps

1. **Load Raw Data into PostgreSQL**  
   - Python script reads JSON files from the data lake  
   - Loads data into `raw.telegram_messages` table

2. **Staging Models** (`models/staging/`)  
   - Clean and standardize raw data  
   - Cast data types correctly (dates, integers, etc.)  
   - Rename columns for consistency  
   - Filter invalid records (empty messages, nulls)  
   - Add calculated fields like `message_length` and `has_image`  

3. **Star Schema** (`models/marts/`)  

**Dimension Tables**
- `dim_channels`: Telegram channel information  
  - Fields: `channel_key`, `channel_name`, `channel_type`, `first_post_date`, `last_post_date`, `total_posts`, `avg_views`
- `dim_dates`: Date information for analytics  
  - Fields: `date_key`, `full_date`, `day_of_week`, `week_of_year`, `month_name`, `quarter`, `year`, `is_weekend`

**Fact Table**
- `fct_messages`: One row per message  
  - Fields: `message_id`, `channel_key` (FK), `date_key` (FK), `message_text`, `message_length`, `view_count`, `forward_count`, `has_image`

4. **dbt Tests**  
   - Built-in: `unique`, `not_null`, `relationships`  
   - Custom:  
     - `assert_no_future_messages` → ensures no messages have future dates  
     - `assert_positive_views` → ensures view counts are non-negative  

5. **Documentation**  
   - Generated with `dbt docs generate`  
   - Served with `dbt docs serve`  
   - Includes descriptions, lineage, and schema details

---

## Evidence / Screenshots
- **dbt tests passing:** _Insert screenshot here_  
- **dbt docs lineage:** _Insert screenshot here_  
- **Star schema diagram:** _Insert diagram here_  
- **Raw data lake folder structure:** _Insert screenshot here_

---

## Project Status
- Task 1 ✅ Completed  
- Task 2 ✅ Completed  
- All dbt tests ✅ Passed  
- Analytics-ready warehouse built and documented

---



