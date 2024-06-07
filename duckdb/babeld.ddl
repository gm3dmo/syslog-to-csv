CREATE TABLE babeld AS
    SELECT *
    FROM read_json_auto(['babeld-logs/babeld.json', 'babeld-logs/babeld.1.json'], ignore_errors=True);
DESCRIBE babeld;
