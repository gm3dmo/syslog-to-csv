WITH intervals AS (
    SELECT
        DATE_TRUNC('minute', ts)
          - ((EXTRACT(MINUTE FROM ts)::int % 5) * INTERVAL '1 minute') AS interval_5m,
        COUNT(*) AS entries_in_5_min,
        COUNT(*) / 5.0 AS entries_per_minute
    FROM babeld
    GROUP BY 1
    ORDER BY 1
),
ordered AS (
    SELECT
        intervals.*,
        ROW_NUMBER() OVER (ORDER BY interval_5m) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM intervals
)
SELECT interval_5m, entries_in_5_min, entries_per_minute
FROM ordered
WHERE rn NOT IN (1, total_rows)
ORDER BY interval_5m;
