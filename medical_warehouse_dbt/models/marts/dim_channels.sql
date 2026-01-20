with messages as (
    select * from {{ ref('stg_telegram_messages') }}
)

select
    row_number() over () as channel_key,
    channel_name,
    'Medical' as channel_type,  -- adjust if you have type info
    min(date_posted) as first_post_date,
    max(date_posted) as last_post_date,
    count(*) as total_posts,
    avg(view_count) as avg_views
from messages
group by channel_name
