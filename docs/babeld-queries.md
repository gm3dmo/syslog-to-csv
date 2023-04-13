# Babeld Queries

```sql
.mode columns
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', ts) as hour, 
       sum(case when msg = "Timed out reading request body from client" then 1 else 0 end) as timed_out_reading_from_client,
       sum(case when msg like "%is not a valid username or token" then 1 else 0 end) as not_valid_username_or_token,
       sum(case when msg like 'http op done: (403) Permission to%' then 1 else 0 end) as permission_denied,
       sum(case when msg like 'http op done: (403) Your account is suspended. Please login%' then 1 else 0 end) as your_account_is_suspended
FROM babeld GROUP BY hour ORDER BY hour;
```
