CREATE TABLE gitrpcd AS
    SELECT *
    FROM read_json_auto(['system-logs/split-logs-syslog/gitrpcd.json', 'system-logs/split-logs-syslog.1/gitrpcd.json' ], ignore_errors=True);
DESCRIBE gitrpcd;
