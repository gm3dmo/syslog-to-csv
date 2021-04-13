# Syslog to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file into a csv file (Debian 10) but others may work.

## syslog-to-csv
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):


Run `syslog-to-csv.py`:

```
python syslog-to-csv.py /var/log/syslog.1
```
or if you need speed:

```
pypy syslog-to-csv.py /var/log/syslog.1
```

Now you have a `syslog.csv` file in your local directory.


## Next Steps

- Process the csv with [csvkit]https://csvkit.readthedocs.io/en/latest/)

### Visualise syslog
Now that you have a csv you can use a wide range of tools like Pandas, and friends or even Excel to interpret your syslog data:

![Syslog Visualized](images/syslog-visualized.png)
