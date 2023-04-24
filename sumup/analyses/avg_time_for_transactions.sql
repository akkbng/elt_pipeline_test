--Average time for a store to perform its 5 first transactions
with transactions as (
    select * from {{ ref('transactions') }}
)

SELECT 
  store_id, 
  AVG(TIMESTAMP_DIFF(created_at, happened_at, SECOND)) AS avg_time
FROM (
  SELECT 
    *,
    ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY happened_at) AS rn
  FROM transactions
) t
WHERE rn <= 5
AND status = 'accepted'
GROUP BY store_id
ORDER BY store_id
