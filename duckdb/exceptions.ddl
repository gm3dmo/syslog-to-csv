CREATE TABLE exceptions AS
    SELECT *
    FROM read_json_auto('github-logs/exceptions.log', ignore_errors=True);
DESCRIBE exceptions;
