SELECT  ABS(ROUND(1. - (x.price*2./(y.price + z.price)), 3)*100) || '%' as deviation
FROM(

WITH tmp as
(
SELECT (event -> 'args' ->> 'current') ::numeric as contract_price,
event -> 'args' ->> 'roundId' as round_id,
event ->> 'transactionIndex' as trans_index,
event -> 'args' ->> 'updatedAt' as updated_at,
event ->> 'blockNumber' as block_number
FROM contract_price
WHERE event ->> 'event_type' = 'link-usd' AND event ->> 'blockNumber' =
(
select max(event ->> 'blockNumber') as max_block_number
FROM contract_price WHERE event ->> 'event_type' = 'link-usd'
)
)
SELECT contract_price/100000000. as price FROM tmp
WHERE tmp.trans_index =
(
select max(trans_index) as max_trans_index
FROM tmp
)
) x

JOIN
(SELECT (event -> 'chainlink' ->> 'usd')::numeric as price
FROM api_price WHERE event ->> 'event_type' = 'cg' order by updated_at desc limit 1
) y

ON 1=1

JOIN(
SELECT (event ->> 'close')::numeric as price
FROM api_price WHERE event ->> 'event_type' = 'cp-link-usd'
order by updated_at desc limit 1
) z

ON 1=1