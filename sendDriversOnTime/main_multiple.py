import stuart.db
import sys
import qs
import pandas as pd
import constants as c
import matplotlib.pyplot as plt
import datetime as dt
import time
import pprint as pp


def fetch_data(job_type, city_or_cid, is_city, date, tt):
    if job_type == c.PU:
        # Using the Redshift Datawarehouse
        con_wh = stuart.db.get_readonly_engine_for_stuart_warehouse()

        # Route the query when it's city or client_id based
        if is_city:
            db_qs = qs.qs_pu_date_city.format(e=city_or_cid, date=date)
        else:
            db_qs = qs.qs_pu_date_cid.format(e=city_or_cid, date=date)

    # DO
    elif job_type == c.DO:
        # Using the StuartBI
        con_wh = stuart.db.get_engine_for_stuart_backend()

        # Route the query when it's city or client_id based
        if is_city:
            db_qs = qs.qs_do_date_city.format(e=city_or_cid, date=date)
        else:
            db_qs = qs.qs_do_date_cid.format(e=city_or_cid, date=date)

    else:
        raise ValueError('Job type not catch earlier. Value provided: {}'.format(job_type))

    t0 = time.time()
    data = pd.read_sql(db_qs, con_wh)
    print('Query execution time: {} sec ({})'.format(round(number=time.time() - t0, ndigits=1), date))

    return data[data.tt == tt]


def check_job_type(v):
    """
    Check if the job type is correct.

    :param v: job type from sys.argv
    :return: raise or continue
    """
    if v not in c.JOB_TYPES:
        raise ValueError('Wrong job type ({}) value. Should be in {}'.format(v, c.JOB_TYPES))
    return v

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


def check_plot_type(v):
    """
    Check the plot type desired (kde / hist)

    :param v: plot type parameter
    :return: v
    """
    if v not in c.PLOT_TYPES:
        raise ValueError('Wrong plot type ({}) value. Should be in {}'.format(v, c.PLOT_TYPES))
    return v


def main():
    job_type = check_job_type(sys.argv[1]) # do/pu?
    city_or_cid = sys.argv[2]
    plot_type = check_plot_type(sys.argv[3])
    is_city = check_is_city(city_or_cid)

    tt = sys.argv[4]
    if tt not in c.TT:
        raise ValueError('Unrecognised TT value ({})'.format(tt))

    dates = sys.argv[5:]
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

    dates_formatted = []
    for date in dates:

        data = fetch_data(job_type, city_or_cid, is_city, date, tt)
        if len(data) < 2:
            print('date {} with TT {} not computable (length < 2)'.format(date, tt))
            continue

        dates_formatted.append('{} {} jobs'.format(dt.datetime.strftime(date, '%Y-%m-%d'), str(len(data))))
        if plot_type == c.KDE:
            data.computed_delta.plot.kde(bw_method=c.BW_METHOD,
                                         xlim=c.XLIM,
                                         figsize=c.FIGSIZE,
                                         xticks=range(c.XLIM[0], c.XLIM[1]+1, 3),
                                         grid=True)

        elif plot_type == c.HIST:
            # Move from seconds to minutes
            computed_delta = data.computed_delta / 60.0
            computed_delta.plot.hist(bins=range(c.XLIM[0], c.XLIM[1]+1, 1),
                                     alpha=c.HIST_ALPHA,
                                     figsize=c.FIGSIZE,
                                     xticks=range(c.XLIM[0], c.XLIM[1] + 1, 3),
                                     grid=True)

        else:
            raise ValueError('Plot type not catch earlier. Value provided: {}'.format(plot_type))

    plt.legend(dates_formatted, loc='best')
    # Indicates the PU time window
    plt.axvline(x=0)
    plt.axvline(x=c.TIME_WINDOW_JOB_TYPE[job_type])
    plt.savefig('charts/multiple_dist/{ts}_dist_{job_type}_{city_or_cid}_{tt}_{bw_method}.png'.format(
        ts=dt.datetime.now().strftime('%Y-%m-%dT%H%M%S'),
        job_type=job_type,
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