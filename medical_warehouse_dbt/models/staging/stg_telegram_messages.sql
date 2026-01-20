with raw as (
    select *
    from raw.telegram_messages
)

select
    message_id,
    channel_name,
    message_text,
    message_date as date_posted,
    coalesce(views, 0)::int as view_count,
    coalesce(forwards, 0)::int as forward_count,
    has_media as has_image,
    length(message_text) as message_length
from raw
where message_text is not null


