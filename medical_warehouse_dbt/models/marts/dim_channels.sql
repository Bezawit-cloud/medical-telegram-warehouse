with messages as (

    select
        channel_name,
        message_date
    from {{ ref('stg_telegram_messages') }}

)

select
    row_number() over (order by channel_name) as channel_key,
    channel_name,
    min(message_date) as first_post_date,
    max(message_date) as last_post_date,
    count(*) as total_messages
from messages
group by channel_name
