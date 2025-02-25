.mode csv
WITH pack_counts AS (
    SELECT 
        cmd, 
        COUNT(*) AS count_cmd
    FROM babeld
    WHERE cmd IN ('git-upload-pack', 'git-receive-pack')
    GROUP BY cmd
),
total AS (
    SELECT SUM(count_cmd) AS total_count
    FROM pack_counts
)
SELECT 
    p.cmd,
    p.count_cmd,
    ROUND(CAST(p.count_cmd AS DOUBLE) / t.total_count * 100, 2) AS percentage
FROM pack_counts p
CROSS JOIN total t
ORDER BY p.count_cmd DESC;
