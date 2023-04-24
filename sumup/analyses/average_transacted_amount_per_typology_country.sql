--Average transacted amount per store typology and country
with stores as (
    select * from {{ ref('stg_stores') }}
),
devices as (
    select * from {{ ref('stg_devices') }}
),
transactions as (
    select * from {{ ref('stg_transactions') }}
)

SELECT s.typology, s.country, AVG(t.amount) as avg_amount
FROM stores s
JOIN devices d ON s.store_id = d.store_id
JOIN transactions t ON d.device_id = t.device_id
GROUP BY s.typology, s.country
