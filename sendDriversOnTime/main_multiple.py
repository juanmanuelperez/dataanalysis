import stuart.db
import sys
import os
import qs
import pandas as pd
import constants as c
import matplotlib.pyplot as plt
import datetime as dt
import time
import pprint as pp


def fetch_data(job_type, city_or_cid, is_city, date, tt):
    con_wh = stuart.db.get_engine_for_stuart_backend()

    if job_type == c.PU:
        # Route the query when it's city or client_id based
        if is_city:
            db_qs = qs.qs_pu_date_city.format(e=city_or_cid, date=date)
        else:
            db_qs = qs.qs_pu_date_cid.format(e=city_or_cid, date=date)

    # DO
    elif job_type == c.DO:
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


def create_dir():
    """
    Create the directory to store the charts.
    """
    dirpath = c.DATA_DIR_PATH.format(dt.datetime.now().strftime('%Y-%m-%dT%H%M%S'))
    try:
        os.mkdir(dirpath)
    except OSError as e:
        raise ValueError('Impossible to create directory. Erro: {}'.format(e))

    return dirpath

def main():
    # Command example
    # python main_multiple.py pu Barcelona hist bike 2019-04-01 2019-04-05
    job_type = check_job_type(sys.argv[1])  # do/pu?
    city_or_cid = sys.argv[2]
    plot_type = check_plot_type(sys.argv[3])
    is_city = check_is_city(city_or_cid)

    tt = sys.argv[4]
    if tt not in c.TT + [c.ALL]:  # Check also it's in ALL but not add it to the normal list
        raise ValueError('Unrecognised TT value ({})'.format(tt))

    # Setup the transport type for it to be in a list to be looped.
    if tt == c.ALL:
        tts = c.TT

    else:
        tts = [tt]

    dates = sys.argv[5:]
    if len(dates) < 2:
        raise ValueError('Need at least 2 dates to compare distributions.')
    elif len(dates) == 2:
        start, end = dt.datetime.strptime(dates[0], '%Y-%m-%d'), dt.datetime.strptime(dates[1], '%Y-%m-%d')

        if end <= start:
            raise ValueError('Invalid end date <= start date (start: {}, end: {}'.format(start, end))

        days = (end - start).days
        dates = [start]  # init the dates list

        for i in range(days):
            dates.append(dates[-1] + dt.timedelta(days=1))

    # Use to create the folder to store the charts
    dirpath = create_dir()

    # Looping through each transport type
    for tt in tts:
        print('\n[Processing TT {}]'.format(tt))

        # Used to decided whether to plot the figures. Requires at least one date with data.
        savefig = []

        dates_formatted = []
        for date in dates:
            print('\tProcessing date {}'.format(date))

            data = fetch_data(job_type, city_or_cid, is_city, date, tt)
            if len(data) < 2:
                print('\t...data not computable (length < 2)')

                # No nada available for this date.
                savefig.append(False)
                continue

            # Data is available for this date.
            savefig.append(True)

            dates_formatted.append('{} {} jobs'.format(dt.datetime.strftime(date, '%Y-%m-%d'), str(len(data))))

            # Move from seconds to minutes
            computed_delta = data.computed_delta / 60.0

            if plot_type == c.KDE:
                computed_delta.plot.kde(bw_method=c.BW_METHOD,
                                        xlim=c.XLIM,
                                        figsize=c.FIGSIZE,
                                        xticks=range(c.XLIM[0], c.XLIM[1]+1, 3),
                                        grid=True)

            elif plot_type == c.HIST:
                computed_delta.plot.hist(bins=range(c.XLIM[0], c.XLIM[1]+1, 1),
                                         alpha=c.HIST_ALPHA,
                                         figsize=c.FIGSIZE,
                                         xticks=range(c.XLIM[0], c.XLIM[1] + 1, 3),
                                         grid=True)

            else:
                raise ValueError('Plot type not catch earlier. Value provided: {}'.format(plot_type))

        if any(savefig):
            plt.legend(dates_formatted, loc='best')
            # Indicates the PU time window
            plt.axvline(x=0)
            plt.axvline(x=c.TIME_WINDOW_JOB_TYPE[job_type])
            plt.savefig(dirpath + '{plot_type}_{job_type}_{city_or_cid}_{tt}_{bw_method}.png'.format(
                plot_type=plot_type,
                job_type=job_type,
                city_or_cid=city_or_cid,
                tt=tt,
                bw_method=c.BW_METHOD),
                        bbox_inches='tight',
                        orientation='portrait')
            plt.clf()
            print('[Figure saved for current date]')
        else:
            print('[Figure not saved for current date (no {} in {})]'.format(tt, city_or_cid))


if __name__ == '__main__':
    """
    Compare KDE between TT and multiple dates.
    """
    main()
    #  17h40