### unicorn.log

#### Top 20 unicorn current_user

```sql
select current_user, COUNT(current_user) as count_current_user from unicorn group by current_user order by count_current_user desc limit 20;
```

#### Top 20 by current_user by hour

```sql
SELECT strftime ('%Y-%m-%d %H',now) by_hour,  current_user, count(current_user)  as count_of_current_user  from unicorn group by strftime ('%H',now), current_user order by count_of_current_user desc limit 20;
```

#### Current_user by hour

```sql
SELECT strftime ('%Y-%m-%d %H',now) by_hour,  current_user, count(current_user)  as count_of_current_user  from unicorn group by strftime ('%H',now), current_user 
```

### Top 20 unicorn users and their "routes"

```sql
select current_user, route, COUNT(current_user) as count_current_user from unicorn group by current_user, route order by count_current_user desc limit 20;
```

#### Rate limiting: Find rate limit of users and count where rate_limit_remaining is 0:

```sql
select rate_limit, current_user, count(current_user) as ct from unicorn where rate_limit_remaining = 0 group by current_user order by ct desc;
```

#### Rate limiting: rate limit applied to each user

```sql
select rate_limit, current_user, count(current_user) as ct from unicorn group by rate_limit;
```

#### Find and count user agent for a particular user "XYZ" and order by hour

```sql
SELECT strftime ('%Y-%m-%d %H',now) by_hour,  user_agent, count(user_agent)  as ct  from unicorn where current_user = 'XYZ' group by strftime ('%H',now), user_agent;
```

#### sum of user XYX by user agent:

```sql
 select sum(count_of_user_agent) as total_from_user from(SELECT strftime('%Y-%m-%d %H',now) by_hour,  auth_fingerprint, user_agent, count(user_agent) as count_of_user_agent, remote_address  from unicorn where current_user = 'XYZ' group by strftime ('%H',now), user_agent order by by_hour asc);
```


```sql
SELECT strftime ('%Y-%m-%d %H:%M',now) hour_min,  user_agent, count(user_agent)  as ct  from unicorn where status = 500 group by strftime ('%H:%M',now), user_agent;
```

```sql
.headers on
.mode columns
.width 0 0 0
SELECT strftime ('%Y-%m-%d %H:%M',now) hour_min,  user_agent, count(user_agent)  as ct  from unicorn where status = 500 group by strftime ('%H:%M',now), user_agent;
```

```sql
SELECT strftime ('%Y-%m-%d %H:%M',now) hour_min,  user_agent, count(user_agent)  as ct  from unicorn where status like '5%' group by strftime ('%H:%M',now), user_agent;
```



```sql
SELECT strftime ('%Y-%m-%d %H:%M',now) hour_min,  status, count(status)  as ct  from unicorn where status = 500 group by strftime ('%H:%M',now), status order by hour_min;
```
