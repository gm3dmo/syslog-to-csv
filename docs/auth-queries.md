## Sample Queries for auth.log

#### Top 20 IP's in auth.log by percentage

```sql
create view percentage_of_ip as select ip, round(100.0 * count() / (select count() from auth), 2) as Percentage from auth group by ip;
.mode csv
.headers on
select * from percentage_of_ip order by Percentage desc limit 20;
```
