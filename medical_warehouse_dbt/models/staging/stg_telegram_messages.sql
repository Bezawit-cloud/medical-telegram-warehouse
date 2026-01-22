-- models/staging/stg_telegram_messages.sql
select
    message_id,
    channel_name,              -- 👈 MUST EXIST HERE
    message_date,
    message_text,
    has_media,
    media_type,
    views,
    forwards
from {{ source('raw', 'telegram_messages') }}

