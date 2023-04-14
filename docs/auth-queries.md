## Sample Queries for auth.log

### Where (IP Address)

#### Top 20 IP's in auth.log by percentage

```sql
drop view percentage_of_ip
create view percentage_of_ip as select ip, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by ip;
.mode columns

.width 20 10
.headers on
select * from percentage_of_ip order by percentage desc limit 20;
```

### Who (login, user_id, raw_login, user_agent)

#### Top 20 `login`'s in auth.log by percentage

```sql
drop view percentage_of_login;
create view percentage_of_login as select login, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by login;

.mode columns
.width 20 10
.headers on

select * from percentage_of_login order by percentage desc limit 20;
```

##### Example

```
login                 count_of    percentage
--------------------  ----------  ----------
jenkins               2644365     11.4
circleci              1696393     7.32
johndoe               1166605     5.03
github-bot            1146013     4.94
```


#### Top 20 `user_id`'s in auth.log by percentage

```sql
drop view percentage_of_user_id;
create view percentage_of_user_id as select login, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by user_id;

.mode columns
.width 20 10
.headers on

select * from percentage_of_user_id order by percentage desc limit 20;
```

#### Top 20 `raw_login`'s in auth.log by percentage

```sql
drop view percentage_of_raw_login;
create view percentage_of_raw_login as select raw_login, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by raw_login;

.mode columns
.width 20 10
.headers on

select * from percentage_of_raw_login order by percentage desc limit 20;
```




#### Top 20 `user_agent`'s in auth.log by percentage

```sql
drop view percentage_of_user_agent;
create view percentage_of_user_agent as select user_agent, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by user_agent;

.mode columns
.width 20 10
.headers on

select * from percentage_of_user_agent order by percentage desc limit 20;
```

### Location (repo, url)

#### Top 20 `repo`'s in auth.log by percentage

```sql
drop view percentage_of_repo;
create view percentage_of_repo as select repo, count() as count_of,round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by repo;

.mode columns
.width 60 10
.headers on

select * from percentage_of_repo order by percentage desc limit 20;
```

#### Top 20 `url`'s in auth.log by percentage

```sql
create view percentage_of_url as select url, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by url;

.mode columns
.width 50 10
.headers on

select * from percentage_of_url order by percentage desc limit 20;
```






### Failures

#### Top 20 `failure_type`'s in auth.log by percentage

```sql
drop view percentage_of_failure_type;
create view percentage_of_failure_type as select failure_type, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by failure_type;

.mode columns
.width 20 10
.headers on

select * from percentage_of_failure_type order by percentage desc limit 20;
```



#### Top 20 `failure_reason`'s in auth.log by percentage

```sql
drop view percentage_of_failure_reason;
create view percentage_of_failure_reason as select failure_reason, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by failure_reason;

.mode columns
.width 20 10
.headers on

select * from percentage_of_failure_reason order by percentage desc limit 20;
```




#### Top 20 `method`'s in auth.log by percentage

```sql
drop view percentage_of_method;
create view percentage_of_method as select method, count() as count_of, round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by method;

.mode columns
.width 50 10
.headers on

select * from percentage_of_method order by percentage desc limit 20;
```

##### Example method:
```
method                                              percentage
--------------------------------------------------  ----------
GitHub::Authentication::Attempt.log                 99.96
GitHub::Authentication::SAML.rails_authenticate     0.01
SAML::Session.log_change                            0.01
SAML::Session.revoke_on_destroy                     0.01
                                                    0.0
Class.create_user                                   0.0
```

#### Top 20 `from`'s in auth.log by percentage

```sql
drop view percentage_of_from;
create view percentage_of_from as select auth.'from', count() as count_of  round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by auth.'from';

.mode columns
.width 50 10
.headers on
select * from percentage_of_from order by percentage desc limit 20;
```

##### Example from:

```
from                                                percentage
--------------------------------------------------  ----------
api                                                 87.84
git                                                 8.72
internal_api                                        3.31
api_middleware                                      0.09
                                                    0.04
internal_lfs                                        0.0
lfs                                                 0.0
web_api                                             0.0
```

#### Top 20 `protocol`'s in auth.log by percentage

```sql
drop view percentage_of_protocol;
create view percentage_of_protocol as select protocol, count() as count_of(), round(100.0 * count() / (select count() from auth), 2) as percentage from auth group by protocol;

.mode columns
.width 50 10
.headers on

select * from percentage_of_protocol order by percentage desc limit 20;
```
##### Example protocol

```
protocol                                            percentage
--------------------------------------------------  ----------
                                                    91.28
http                                                8.71
svn                                                 0.01
```


### Queries with temporal information

Group by hour, login, message

```sql
.mode columns
.width 15 15 5 90
.headers on
SELECT strftime ('%Y-%m-%d %H',now) hour, login, count(login) as authentications_count, message  from auth where at = 'failure' group by strftime ('%H',now), login, message  order by hour;
```

#### Auth failures by hour

##### LDAP Specific

```sql
.mode columns
.width 60
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', now) as hour, 
      sum(case when message = 'Authentication success via token' then 1 else 0 end) as auth_success_via_token,
      sum(case when message = 'Your account has been suspended. via token' then 1 else 0 end) as account_suspended_via_token,
      sum(case when message = 'Authentication success' then 1 else 0 end) as auth_success,
      sum(case when message = 'Authentication failure' then 1 else 0 end) as auth_failure,
      sum(case when message = 'Authentication failure via token' then 1 else 0 end) as auth_failure_via_token,
      sum(case when message like 'The external%' then 1 else 0 end) as external_auth_server_failed_to_respond,
      sum(case when message = 'Invalid LDAP login credentials.' then 1 else 0 end) as invalid_ldap_login_creds
FROM auth GROUP BY hour ORDER BY hour;
```

##### SAML Specific

```sql
.mode columns
.headers on
.timer on
.width 20 0 0 0
SELECT strftime('%Y-%m-%d %H:00:00', auth.now) as hour, 
      sum(case when message = 'Authentication success via token' then 1 else 0 end) as auth_success_via_token,
      sum(case when message = 'Authentication failure via token' then 1 else 0 end) as auth_failure_via_token,
      sum(case when message = 'Your account has been suspended. via token' then 1 else 0 end) as account_suspended_via_token,
      sum(case when message = 'Authentication success' then 1 else 0 end) as auth_success,
      sum(case when message = 'Authentication failure' then 1 else 0 end) as auth_failure,
      sum(case when message = 'Password authentication is not supported by SAML authentication' then 1 else 0 end) as passwd_auth_not_supported_by_saml,
      sum(case when message like 'Unable to create the user because username is too long%' then 1 else 0 end) as username_too_long
FROM auth GROUP BY hour ORDER BY hour;
```

###### Top 10 of *user_id* logging in most

```sql
.mode columns
.headers on
.timer on
.width 20 0 0 0
SELECT strftime('%Y-%m-%d %H:00:00', auth.now) AS time_period, auth.user_id, count(*) AS count
FROM auth
GROUP BY time_period, auth.user_id
ORDER BY count DESC
LIMIT 10;
```

###### Top 10 hours of *message* logged most

```sql
.mode columns
.headers on
.timer on
.width 20 0 0 0
SELECT strftime('%Y-%m-%d %H:00:00', auth.now) AS time_period, auth.message, count(*) AS count
FROM auth
GROUP BY time_period, auth.message
ORDER BY count DESC
LIMIT 10;
```

###### Top 10 of *login* logging in most

```sql
.mode columns
.headers on
.timer on
.width 20 0 0 0
SELECT strftime('%Y-%m-%d %H:00:00', auth.now) AS time_period, auth.login, count(*) AS count
FROM auth
GROUP BY time_period, auth.login
ORDER BY count DESC
LIMIT 10;
```

