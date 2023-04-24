--Top 10 stores per transacted amount
with stores as (
    select * from {{ ref('stg_stores') }}
),
devices as (
    select * from {{ ref('stg_devices') }}
),
transactions as (
    select * from {{ ref('stg_transactions') }}
)


SELECT s.store_id, SUM(t.amount) AS total_amount
FROM stores s
JOIN devices d ON s.store_id = d.store_id
JOIN transactions t ON d.device_id = t.device_id
WHERE t.status = 'accepted'
GROUP BY s.store_id
ORDER BY total_amount DESC
LIMIT 10;