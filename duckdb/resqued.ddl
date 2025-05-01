.timer on
CREATE TABLE resqued AS
     SELECT * FROM read_csv(['github-logs/resqued.1.csv', 'github-logs/resqued.csv' ]);

DESCRIBE hookshot;
