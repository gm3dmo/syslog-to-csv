

#### Install/Setup `syslog-to-csv`
- Inside the bundle directory `Downloads/github-support-bundle`, download and unzip the latest release of [syslog-to-csv](https://github.com/gm3dmo/syslog-to-csv/releases/latest)
- Run `b2c.py`. This will automatically:
  - Extract all daemon entries to their own files, see `system-logs/split-logs-syslog`.
  - Convert `.log` files to CSV format.
  - Load the CSV format files into a sqlite database named `logs.db`.
- Run a pre-prepared "view" query for a table such as *unicorn*. This will output useful statistics about different facets of the data:

```
bash unicorn.sql
unicorn Summary
---------------
repo                                                          count_of  percentage
------------------------------------------------------------  --------  ----------
                                                              372       50.82
nil                                                           320       43.72
acme/testrepo                                                 28        3.83
roger-de-courcey/who-framed-roger-repo                        11        1.5
ghe-admin/5988458ae3e96ce86959e48caa0eae23                    1         0.14

user                                                          count_of  percentage
------------------------------------------------------------  --------  ----------
                                                              403       55.05
nil                                                           281       38.39
roger-de-courcey                                              23        3.14
ghe-admin                                                     17        2.32
pip-crispy                                                    8         1.09
```

- Open the database (logs.db) with sqlite3 and your own custom queries:

```
sqlite3 logs.db
```

- There are sample queries in the `syslog-to-csv/docs` directory like `auth-queries.md`, `babeld-queries.md`