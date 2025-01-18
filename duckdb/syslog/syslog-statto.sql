.mode csv
SELECT 
    daemon,
    SUM(line_length) as total_length,
    MIN(line_length) as min_length,
    MAX(line_length) as max_length,
    ROUND(AVG(line_length), 2) as avg_length,
    ROUND(STDDEV(line_length), 2) as std_dev,
    ROUND(QUANTILE(line_length, 0.95), 2) as p95,
    COUNT(*) as total_lines
FROM syslog 
GROUP BY daemon 
ORDER BY total_length DESC;
