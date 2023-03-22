#### Install/Setup `syslog-to-csv`
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

#### Run `syslog-to-csv.py`
To create a `syslog.csv` file in the working directory:

```
python3 syslog-to-csv.py /var/log/syslog
```

##### Use pypy for speed
If large files need to be processed more quickly then using [pypy3](https://www.pypy.org/) to replace python provides a very significant speed boost:

```
pypy3 syslog-to-csv.py /var/log/syslog.1
```

