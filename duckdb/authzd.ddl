CREATE TABLE authzd AS
    SELECT *
    FROM read_json_auto(['system-logs/split-logs-syslog/authzd.json', 'system-logs/split-logs-syslog.1/authzd.json' ], ignore_errors=True);
DESCRIBE authzd;
