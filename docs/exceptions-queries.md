### Exceptions

#### Count of class
```sql
select "class", count("class") as count_of_class  from exceptions group by class order by  count_of_class desc;
```


#### Count of user
```sql
select "user", count("user") as count_of_user  from exceptions group by user order by  count_of_user desc;
```

#### Count of controller
```sql
select "controller", count("controller") as count_of_controller  from exceptions group by controller order by  count_of_controller desc;
```

#### Count of cause
```sql
select "cause", count("cause") as count_of_cause  from exceptions group by cause order by  count_of_cause desc;
```

#### Count of exceptions by api_route
```sql
select "api_route", count("api_route") as count_of_api_route  from exceptions group by api_route order by  count_of_api_route desc;
```

### Exceptions by hour

#### created_at

```sql
SELECT strftime ('%Y-%m-%d %H',created_at) by_hour,  class, count(class)  as class_exceptions_count  from exceptions group by class order by class_exceptions_count desc limit 20;
```



#### class by hour

```sql
SELECT strftime ('%Y-%m-%d %H',created_at) hour,  class, count(class)  class_exceptions_count  from exceptions  group by strftime ('%H',created_at), class;
```

