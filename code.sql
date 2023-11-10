select 
	b.security,
    b.price as ask,
    b.Buy as ask_qty,
    s.price as bid,
    s.sell as bid_qty
from (SELECT 
		`security` as security,
		price,
		buy
	FROM quik_quotes q
	where q.buy <> 0 
	order by q.price desc
	limit 1) as b,
	(SELECT 
		`security` as security,
		price,
		sell
	FROM quik_quotes q
	where q.sell <> 0 
	order by q.price asc
	limit 1) s
where b.security = s.security;
