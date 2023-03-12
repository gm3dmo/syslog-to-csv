## Sample Queries for auth.log

#### Top 20 IP's in auth.log by percentage

```sql
create view percentage_of_ip as select ip, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by ip;
.mode columns

.width 20 10
.headers on
select * from percentage_of_ip order by percentage desc limit 20;
```

#### Top 20 `repo`'s in auth.log by percentage

```sql
create view percentage_of_repo as select repo, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by repo;

.mode columns
.width 60 10
.headers on

select * from percentage_of_repo order by percentage desc limit 20;
```

#### Top 20 `failure_reason`'s in auth.log by percentage

```sql
create view percentage_of_failure_reason as select failure_reason, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by failure_reason;

.mode columns
.width 20 10
.headers on

select * from percentage_of_failure_reason order by percentage desc limit 20;
```


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
