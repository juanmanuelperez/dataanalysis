qs_pu_date_city = """
select
j.job_id as job_id
,j.transport_type as tt
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as computed_delta

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

qs_pu_date_cid = """
select
j.job_id as job_id
,j.transport_type as tt
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as computed_delta

from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id

where
j.client_id = {e}
and date(j.job_created_at)= '{date}'
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
"""

qs_do_date_city = """
select
	job.id as job_id,
	case
		when job.transport_type_id=1 then 'walk'
		when job.transport_type_id=2 then 'bike'
		when job.transport_type_id=3 then 'motorbike'
		when job.transport_type_id=4 then 'car'
		when job.transport_type_id=5 then 'cargobike'
		when job.transport_type_id=6 then 'van'
		when job.transport_type_id=7 then 'cargobike_xl'
		when job.transport_type_id=8 then 'motorbike_xl'
		else 'unknown'
	end as tt,
	job.client_id as client_id,
	job.status as job_status,
	zones.code as city,
	delivery_status.created_at as almost_delivering_at,
	job.dropoff_at as dropoff_at,
	timestampdiff(second, job.dropoff_at, delivery_status.created_at) as computed_delta

from job
left join delivery on job.id=delivery.job_id
left join delivery_status on delivery.id=delivery_status.delivery_id
left join zones on job.zone_id=zones.id

where
    date(job.start_inviting_at)='{date}'
    and zones.code='{e}'
    and delivery_status.status='almost_delivering'
    and job.status='finished'
    and job.dropoff_at is not null
"""

qs_do_date_cid = """
select
	job.id as job_id,
	case
		when job.transport_type_id=1 then 'walk'
		when job.transport_type_id=2 then 'bike'
		when job.transport_type_id=3 then 'motorbike'
		when job.transport_type_id=4 then 'car'
		when job.transport_type_id=5 then 'cargobike'
		when job.transport_type_id=6 then 'van'
		when job.transport_type_id=7 then 'cargobike_xl'
		when job.transport_type_id=8 then 'motorbike_xl'
		else 'unknown'
	end as tt,
	job.client_id as client_id,
	job.status as job_status,
	zones.code as city,
	delivery_status.created_at as almost_delivering_at,
	job.dropoff_at as dropoff_at,
	timestampdiff(second, job.dropoff_at, delivery_status.created_at) as computed_delta

from job
left join delivery on job.id=delivery.job_id
left join delivery_status on delivery.id=delivery_status.delivery_id
left join zones on job.zone_id=zones.id

where
    date(job.start_inviting_at)='{date}'
    and job.client_id={e}
    and delivery_status.status='almost_delivering'
    and job.status='finished'
    and job.dropoff_at is not null
"""