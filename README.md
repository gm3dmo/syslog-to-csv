### Syslog to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file to Comma Separated Values (CSV) format using [Python 3](https://python.org)  This has been tested with Debian 10 and AWS Linux but other syslog formats will probably work.

#### Install/Setup `syslog-to-csv`
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

#### Run `syslog-to-csv.py`
To create a `syslog.csv` file in the working directory:

```
python3 syslog-to-csv.py /var/log/syslog
```

##### Using pypy for speed
If large files need to be processed more quickly then [pypy3](https://www.pypy.org/) can be used instead of python:

```
pypy3 syslog-to-csv.py /var/log/syslog.1
```

##### Debug mode
Debug mode will print out details of each line as it is processed:

```
python3 -d syslog-to-csv.py /var/log/syslog
```

##### Skipped lines
If a line in the syslog input cannot be processed for some reason then an ERROR will be raised and the line will be skipped:


```
ERROR:syslog-to-csv:Could not parse: 2 (check resulted in Dispatch Password Requests to Console Directory Watch being skipped.)
ERROR:syslog-to-csv:squib: line 4 does not have host/daemon portion.
ERROR:syslog-to-csv:Could not parse: 9 (1900-00-30 07:03:29.68 line 4 runtime (CLR) functionality initialized.)
ERROR:syslog-to-csv:squib: line 10 is not minimum length of (15) characters
```


##### Next Steps
With the data in CSV format a wide range of tools like Pandas, Sqlite or Excel can be used to interpret the syslog data. For example, this little chart was created using Pandas:

- Process the csv with [csvkit](https://csvkit.readthedocs.io/en/latest/) to get a summary of it's contents.


![Syslog Visualized](images/syslog-visualized.png)
