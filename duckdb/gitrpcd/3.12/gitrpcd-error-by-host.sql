.mode csv
select host, error, count() count_error from gitrpcd where error != '' group by host, error order by count_error desc limit 20;
