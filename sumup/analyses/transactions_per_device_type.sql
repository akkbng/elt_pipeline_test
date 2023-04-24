--Percentage of transactions per device type
with transactions as (
    select * from {{ ref('transactions') }}
)

SELECT 
  type,
  COUNT(*) as transaction_count,
  COUNT(*) / SUM(COUNT(*)) OVER() * 100 as percentage
FROM transactions
GROUP BY type
ORDER BY type;