/*
### Which user/repo/banner  are "bad command" messages coming from in the babeld.log?
*/

.headers on
.mode column
.width 20 30 20
select creason, user, msg, log_level, repo, banner, count(creason) as count_of_bad_command from babeld 
where creason like 'bad command' 
group by creason, user_agent, repo 
order by count_of_bad_command desc 
limit 50;

/* show timespan of babeld.log */
SELECT  min(ts) as "first_record", 
        max(ts) as "last_record",  
        printf("%.2f", JULIANDAY(max(ts)) - JULIANDAY(min(ts))) AS "babeld log span (days)" 
from babeld where ts != '';