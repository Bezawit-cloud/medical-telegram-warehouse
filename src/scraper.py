# src/scraper.py

import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError, RPCError

# =========================
# 1. ENV & CLIENT SETUP
# =========================
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("session", API_ID, API_HASH)

# =========================
# 2. PATH CONFIGURATION
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]

TODAY = datetime.now().strftime("%Y-%m-%d")

RAW_MESSAGES_DIR = BASE_DIR / "data/raw/telegram_messages" / TODAY
RAW_IMAGES_DIR = BASE_DIR / "data/raw/images"
LOGS_DIR = BASE_DIR / "logs"

RAW_MESSAGES_DIR.mkdir(parents=True, exist_ok=True)
RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 3. LOGGING SETUP
# =========================
logging.basicConfig(
    filename=LOGS_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# =========================
# 4. CHANNEL SCRAPER
# =========================
async def scrape_channel(channel_name: str, limit: int = 300, max_retries: int = 3):
    """
    Scrape messages and images from a public Telegram channel
    and store them in a raw data lake.
    """
    retries = 0

    while retries < max_retries:
        try:
            logging.info(f"Starting scrape for channel: {channel_name}")
            print(f"Scraping {channel_name}...")

            entity = await client.get_entity(channel_name)
            messages = []

            channel_image_dir = RAW_IMAGES_DIR / channel_name
            channel_image_dir.mkdir(parents=True, exist_ok=True)

            async for msg in client.iter_messages(entity, limit=limit):
                msg_data = {
                    "message_id": msg.id,
                    "date": msg.date.isoformat() if msg.date else None,
                    "text": msg.text,
                    "views": msg.views,
                    "forwards": msg.forwards,
                    "has_media": msg.media is not None,
                    "media_type": type(msg.media).__name__ if msg.media else None,
                }

                # Download image if it doesn't exist
                if msg.photo:
                    image_path = channel_image_dir / f"{msg.id}.jpg"
                    if not image_path.exists():  # safe: do not re-download
                        await msg.download_media(file=image_path)

                messages.append(msg_data)

                if msg.id % 50 == 0:
                    logging.info(f"{channel_name}: processed message {msg.id}")

            # Save raw JSON (one file per channel per day)
            output_file = RAW_MESSAGES_DIR / f"{channel_name}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

            logging.info(
                f"Finished scraping {channel_name}. "
                f"Total messages: {len(messages)}"
            )
            print(f"Finished scraping {channel_name}. Total messages: {len(messages)}")
            break

        except FloodWaitError as e:
            logging.warning(
                f"Flood wait for {channel_name}: sleeping {e.seconds} seconds"
            )
            await asyncio.sleep(e.seconds)
            retries += 1

        except RPCError as e:
            logging.error(f"RPC error for {channel_name}: {e}")
            retries += 1
            await asyncio.sleep(5)

        except Exception as e:
            logging.error(f"Unexpected error for {channel_name}: {e}")
            retries += 1
            await asyncio.sleep(5)

    if retries == max_retries:
        logging.error(f"Failed to scrape {channel_name} after {max_retries} retries")

# =========================
# 5. MAIN RUNNER
# =========================
async def main():
    await client.start()

    channels = [
        "lobelia4cosmetics",  # will recreate JSON
        "tikvahpharma",       # will recreate JSON
        "CheMed123",          # new channel
    ]

    for channel in channels:
        # Always recreate JSON, but skip downloading images if they exist
        await scrape_channel(channel)

    await client.disconnect()

# =========================
# 6. ENTRY POINT
# =========================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # For environments with a running event loop (e.g., Jupyter)
        import nest_asyncio

        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())


