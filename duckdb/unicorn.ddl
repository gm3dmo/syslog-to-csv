.timer on
CREATE TABLE unicorn AS
     SELECT * FROM read_csv(['github-unicorn.csv' ]);

DESCRIBE unicorn;
