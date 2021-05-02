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
If a line in the syslog input cannot be processed for some reason then a 

##### Next Steps
With the data in CSV format a wide range of tools like Pandas, Sqlite or Excel can be used to interpret the syslog data. For example, this little chart was created using Pandas:

- Process the csv with [csvkit](https://csvkit.readthedocs.io/en/latest/) to get a summary of it's contents.


![Syslog Visualized](images/syslog-visualized.png)
