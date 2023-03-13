## Sample Queries for auth.log

### Where (IP Address)

#### Top 20 IP's in auth.log by percentage

```sql
create view percentage_of_ip as select ip, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by ip;
.mode columns

.width 20 10
.headers on
select * from percentage_of_ip order by percentage desc limit 20;
```

### Who (raw_login, user_agent)

#### Top 20 `raw_login`'s in auth.log by percentage

```sql
create view percentage_of_raw_login as select raw_login, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by raw_login;

.mode columns
.width 20 10
.headers on

select * from percentage_of_raw_login order by percentage desc limit 20;
```

#### Top 20 `user_agent`'s in auth.log by percentage

```sql
create view percentage_of_user_agent as select user_agent, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by user_agent;

.mode columns
.width 20 10
.headers on

select * from percentage_of_user_agent order by percentage desc limit 20;
```

### Location (repo, url)

#### Top 20 `repo`'s in auth.log by percentage

```sql
create view percentage_of_repo as select repo, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by repo;

.mode columns
.width 60 10
.headers on

select * from percentage_of_repo order by percentage desc limit 20;
```

#### Top 20 `url`'s in auth.log by percentage

```sql
create view percentage_of_url as select url, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by url;

.mode columns
.width 50 10
.headers on

select * from percentage_of_url order by percentage desc limit 20;
```






### Failures

#### Top 20 `failure_type`'s in auth.log by percentage

```sql
create view percentage_of_failure_type as select failure_type , round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by failure_type;

.mode columns
.width 20 10
.headers on

select * from percentage_of_failure_type order by percentage desc limit 20;
```



#### Top 20 `failure_reason`'s in auth.log by percentage

```sql
create view percentage_of_failure_reason as select failure_reason, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by failure_reason;

.mode columns
.width 20 10
.headers on

select * from percentage_of_failure_reason order by percentage desc limit 20;
```




#### Top 20 `method`'s in auth.log by percentage

```sql
create view percentage_of_method as select method, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by method;

.mode columns
.width 50 10
.headers on

select * from percentage_of_method order by percentage desc limit 20;
```
#### Top 20 `from`'s in auth.log by percentage

```sql
create view percentage_of_from as select auth.'from', round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by auth.'from';

.mode columns
.width 50 10
.headers on

select * from percentage_of_from order by percentage desc limit 20;
```



#### Top 20 `protocol`'s in auth.log by percentage

```sql
drop view percentage_of_protocol;
create view percentage_of_protocol as select protocol, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by protocol;

.mode columns
.width 50 10
.headers on

select * from percentage_of_protocol order by percentage desc limit 20;
```
