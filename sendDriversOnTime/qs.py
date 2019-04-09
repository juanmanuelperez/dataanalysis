qs_city_date = """
select
j.job_id as job_id
,j.transport_type as tt
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as almost_picking_at_vs_pickup_at

from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id

where
j.city = '{e}'
and date(j.job_created_at)= '{date}'
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
"""

qs_cid_date = """
select
j.job_id as job_id
,j.transport_type as tt
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as almost_picking_at_vs_pickup_at

from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id

where
j.client_id = '{e}'
and date(j.job_created_at)= '{date}'
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
"""