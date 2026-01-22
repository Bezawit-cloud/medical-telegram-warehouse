select
    m.message_id,
    d.channel_key,
    m.message_date,
    length(m.message_text) as message_length,
    m.has_media,
    m.views,
    m.forwards
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} d
  on m.channel_name = d.channel_name
