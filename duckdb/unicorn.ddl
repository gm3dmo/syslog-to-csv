CREATE TABLE unicorn AS
    SELECT *
    FROM read_json_auto('docker/container-logs/github-unicorn.json', ignore_errors=True);
DESCRIBE unicorn;
