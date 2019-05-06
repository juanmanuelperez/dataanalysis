import stuart.db
import time
import qs
import sys
import pandas as pd


def get_data(job_type, city_or_cid, is_city, date, tt):
    con_wh = stuart.db.get_engine_for_stuart_backend()

    # Route the query when it's city or client_id based
    if is_city:
        db_qs = qs.qs_pu_date_city.format(e=city_or_cid, date=date)
    else:
        db_qs = qs.qs_pu_date_cid.format(e=city_or_cid, date=date)


    t0 = time.time()
    data = pd.read_sql(db_qs, con_wh)
    print('Query execution time: {} sec ({})'.format(round(number=time.time() - t0, ndigits=1), date))

    return data[data.tt == tt]

def check_is_city(v):
    """
    Check either the command line requests a city or a client.

    :param v: city or client_id being requested
    :return: boolean whether it's a city
    """
    try:
        _ = int(v)
        return False
    except Exception:
        return True


if __name__ == '__main__':
    city_or_cid = sys.argv[1]
    is_city = check_is_city(city_or_cid)

