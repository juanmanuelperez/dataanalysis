import stuart.db
import sys
import qs
import pandas as pd
import constants as c
import matplotlib.pyplot as plt
import datetime as dt
import pprint as pp


def fetch_data(city_or_cid, is_city, date, tt):
    con_wh = stuart.db.get_readonly_engine_for_stuart_warehouse()

    # Route the query when it's city or client_id based
    if is_city:
        db_qs = qs.qs_city_date.format(e=city_or_cid, date=date)
    else:
        db_qs = qs.qs_cid_date.format(e=city_or_cid, date=date)

    data = pd.read_sql(db_qs, con_wh)

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


def main():
    city_or_cid = sys.argv[1]
    is_city = check_is_city(city_or_cid)

    tt = sys.argv[2]
    if tt not in c.TT:
        raise ValueError('Unrecognised TT value ({})'.format(tt))

    dates = sys.argv[3:]
    if len(dates) < 2:
        raise ValueError('Need at least 2 dates to compare distributions.')
    elif len(dates) == 2:
        start, end = dt.datetime.strptime(dates[0], '%Y-%m-%d'), dt.datetime.strptime(dates[1], '%Y-%m-%d')

        if end < start:
            raise ValueError('End date strictly before the start date (start: {}, end: {}'.format(start, end))

        days = (end - start).days
        dates = [start] # init the dates list

        for i in range(days):
            dates.append(dates[-1] + dt.timedelta(days=1))

    for date in dates:

        data = fetch_data(city_or_cid, is_city, date, tt)
        if len(data) < 2:
            print('date {} with TT {} not computable (length < 2)'.format(date, tt))
            continue

        data.almost_picking_at_vs_pickup_at.plot.kde(bw_method=c.BW_METHOD,
                                                     xlim=c.XLIM,
                                                     figsize=c.FIGSIZE,
                                                     xticks=range(c.XLIM[0], c.XLIM[1]+1, 3),
                                                     grid=True)

    plt.legend(dates, loc='best')
    # Indicates the PU time window
    plt.axvline(x=0)
    plt.axvline(x=15)
    plt.savefig('charts/multiple_dist/{ts}_dist_{city_or_cid}_{tt}_{bw_method}.png'.format(
        ts=dt.datetime.now().strftime('%Y-%m-%dT%H%M%S'),
        date=date,
        city_or_cid=city_or_cid,
        tt=tt,
        bw_method=c.BW_METHOD),
                bbox_inches='tight',
                orientation='portrait')


if __name__ == '__main__':
    """
    Compare KDE between TT and multiple dates.
    """
    main()
    # 17h40