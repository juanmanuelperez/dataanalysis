qs_pu_date_city = """
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
	delivery_status.created_at as waiting_at_pickup_at,
	job.pickup_at as pickup_at,
	timestampdiff(second, job.pickup_at, delivery_status.created_at) as computed_delta

from job
left join delivery on job.id=delivery.job_id
left join delivery_status on delivery.id=delivery_status.delivery_id
left join zones on job.zone_id=zones.id

where
    date(job.start_inviting_at)='{date}'
    and zones.code='{e}'
    and delivery_status.status='waiting_at_pickup'
    and job.status='finished'
    and job.pickup_at is not null
"""

qs_pu_date_cid = """
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
	delivery_status.created_at as almost_picking_at,
	job.pickup_at as pickup_at,
	timestampdiff(second, job.pickup_at, delivery_status.created_at) as computed_delta

from job
left join delivery on job.id=delivery.job_id
left join delivery_status on delivery.id=delivery_status.delivery_id
left join zones on job.zone_id=zones.id

where
    date(job.start_inviting_at)='{date}'
    and job.client_id={e}
    and delivery_status.status='almost_picking'
    and job.status='finished'
    and job.pickup_at is not null
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