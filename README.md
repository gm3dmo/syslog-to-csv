# Syslog to CSV
[Python 3](https://python.org) to convert a [syslog](https://tools.ietf.org/html/rfc5424) file to Comma Separated Values (CSV) format. This has been tested with Debian 10, AWS Linux but others may work also.

## syslog-to-csv
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

Run `syslog-to-csv.py` to create a `syslog.csv` file:

```
python3 syslog-to-csv.py /var/log/syslog
```

To process the file much more quickly [pypy](https://www.pypy.org/) can be used instead of python:

```
pypy3 syslog-to-csv.py /var/log/syslog.1
```

Now you have a `syslog.csv` file in your local directory.

## Next Steps

- Process the csv with [csvkit](https://csvkit.readthedocs.io/en/latest/) to get a summary of it's contents.

Now that you have a csv you can use a wide range of tools like Pandas, Sqlite or Excel to interpret your syslog data. This little chart was created using pandas for example:

![Syslog Visualized](images/syslog-visualized.png)
