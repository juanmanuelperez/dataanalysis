# List of the cities per country without the main city (Paris / London / Barcelona)
cities = {
    'paris': [
        'Aix-en-Provence',
        'Amiens',
        'Angers',
        'Angoulême',
        'Bordeaux',
        'Brive',
        'Caen',
        'Cannes',
        'Clermont-Ferrand',
        'Dijon',
        'Evreux',
        'Grenoble',
        'Le Havre',
        'Lille',
        'Limoges',
        'Lyon',
        'Marseille',
        'Merignac',
        'Metz',
        'Montpellier',
        'Nancy',
        'Nantes',
        'Nice',
        'Nîmes',
        'Orléans',
        'Paris',
        'Perigueux',
        'Reims',
        'Rennes',
        'Rouen',
        'Saint-Étienne',
        'Strasbourg',
        'Toulouse',
        'Tours'
    ],
    'london': [
        'Basildon',
        'Blackpool',
        'Bournemouth',
        'Brighton',
        'Bristol',
        'Cambridge',
        'Cardiff',
        'Darlington',
        'Derby',
        'Exeter',
        'Gillingham',
        'Huddersfield',
        'Hull',
        'Leeds',
        'Leicester',
        'Liverpool',
        'London',
        'Manchester',
        'Milton Keynes',
        'Newcastle_Gateshead',
        'Northampton',
        'Nottingham',
        'Oxford',
        'Plymouth',
        'Reading',
        'Sheffield',
        'South_Shields',
        'Southampton',
        'Sunderland',
        'Swansea',
        'Teesside',
        'Birmingham',
        'Teesside',
        'Wakefield',
        'Warrington'
    ],
    'barcelona': [
        'Barcelona',
        'Madrid'
    ]
}

country_codes = {
    'paris': 'FR',
    'london': 'UK',
    'barcelona': 'ES'
}

db_querystring = {
    'paris': """
select
/*General Delivery Information*/
j.job_id as job_id
,j.transport_type as tt
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city


/* Time stamps*/
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at


/*Pickup Accuracy*/
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as almost_picking_at_vs_pickup_at


from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id


where
j.city in ('Aix-en-Provence',
        'Amiens',
        'Angers',
        'Angoulême',
        'Bordeaux',
        'Brive',
        'Caen',
        'Cannes',
        'Clermont-Ferrand',
        'Dijon',
        'Evreux',
        'Grenoble',
        'Le Havre',
        'Lille',
        'Limoges',
        'Lyon',
        'Marseille',
        'Merignac',
        'Metz',
        'Montpellier',
        'Nancy',
        'Nantes',
        'Nice',
        'Nîmes',
        'Orléans',
        'Paris',
        'Perigueux',
        'Reims',
        'Rennes',
        'Rouen',
        'Saint-Étienne',
        'Strasbourg',
        'Toulouse',
        'Tours')
and extract(year from j.job_created_at) = '{query_year}'
and extract(week from j.job_created_at) in ({query_week})
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
""",
    'london': """
select
/*General Delivery Information*/
j.job_id as job_id
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city


/* Time stamps*/
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at


/*Pickup Accuracy*/
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as almost_picking_at_vs_pickup_at


from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id


where
j.city in ('Basildon',
        'Blackpool',
        'Bournemouth',
        'Brighton',
        'Bristol',
        'Cambridge',
        'Cardiff',
        'Darlington',
        'Derby',
        'Exeter',
        'Gillingham',
        'Huddersfield',
        'Hull',
        'Leeds',
        'Leicester',
        'Liverpool',
        'London',
        'Manchester',
        'Milton Keynes',
        'Newcastle_Gateshead',
        'Northampton',
        'Nottingham',
        'Oxford',
        'Plymouth',
        'Reading',
        'Sheffield',
        'South_Shields',
        'Southampton',
        'Sunderland',
        'Swansea',
        'Teesside',
        'Birmingham',
        'Teesside',
        'Wakefield',
        'Warrington')
and extract(year from j.job_created_at) = '{query_year}'
and extract(week from j.job_created_at) in ({query_week})
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
""",
    'barcelona': """
select
/*General Delivery Information*/
j.job_id as job_id
,j.client_id as client_id
,j.final_status as final_job_status
,j.city as city


/* Time stamps*/
,dt.almost_picking_at as almost_picking_at
,j.pickup_at as pickup_at


/*Pickup Accuracy*/
,datediff(s,j.pickup_at,dt.almost_picking_at)/60.0 as almost_picking_at_vs_pickup_at


from job j
left join delivery d on j.job_id = d.job_id
left join delivery_times dt on dt.delivery_id = d.delivery_id
left join client c on c.client_id = j.client_id


where
j.city in ('Barcelona', 'Madrid')
and extract(year from j.job_created_at) = '{query_year}'
and extract(week from j.job_created_at) in ({query_week})
and j.final_status = 'finished'
and j.pickup_at is not null
and dt.almost_picking_at is not null

group by 1,2,3,4,5,6,7
"""
}