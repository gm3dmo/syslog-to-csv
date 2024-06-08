.mode csv
.headers on
select count(msg) as count_of_msg, log_level,  msg from babeld group by msg, log_level order by count_of_msg desc limit 20;
