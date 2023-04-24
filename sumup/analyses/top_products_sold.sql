--Top 10 sold products
with transactions as (
    select * from {{ ref('stg_transactions') }}
)

SELECT product_sku, COUNT(*) as total_sold
FROM transactions
GROUP BY product_sku
ORDER BY total_sold DESC
LIMIT 10;