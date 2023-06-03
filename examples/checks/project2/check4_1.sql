SELECT 
    CASE
        WHEN row_count = 0 THEN 0
        ELSE 2
    END as result, 
    *
FROM
(
    SELECT 
        COUNT(*) OVER () as row_count,
        * 
    FROM orders ord
    LEFT JOIN customers cus ON ord.customer_id = cus.customer_id
    WHERE cus.customer_id IS NULL
) t
