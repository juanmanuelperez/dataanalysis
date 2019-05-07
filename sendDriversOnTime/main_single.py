import sys
import stuart.db
import qs
import constants as c
import pandas as pd
import pprint as pp
import matplotlib.pyplot as plt

def clean_df(df):
    """A df with <2 job deliveries is invalid."""
    df_copy = df.copy()
    df_copy = df_copy.groupby('tt')
    to_del = []
    for group in df_copy.groups:
        n = len(df_copy.groups[group])
        if n < 2:
            to_del.append((group, n))

    # Subsetting the initial DF.
    for obj in to_del:
        tt, n = obj
        df = df[df.tt != tt]
    return df

def get_title(name, group):
    title = '{name} (bw_method={bw_method})\n(n={count} mean={mean}, std={std}, min={min}, max={max})'.format(
        name=name,
        bw_method=c.BW_METHOD,
        count=int(group.count()),
        mean=round(group.mean(),1),
        std=round(group.std(),1),
        min=round(group.min(),1),
        max=round(group.max(),1))
    return title

def compute_kde(df, date, city):
    xticks = range(c.XLIM[0], c.XLIM[1]+1, 3)

    df = clean_df(df)
    g = df.groupby('tt').almost_picking_at
    n = g.ngroups
    nrows = n // 2
    if n % 2: # n is odd
        nrows = (n // 2) + 1
    print('Number of groups is {} with TTs: {}'.format(n, list(g.groups.keys())))
    fig, axes = plt.subplots(nrows=nrows, ncols=2, figsize=c.FIGSIZE, sharex=True, sharey=False)
    for i, (name, group) in enumerate(g):
        title = get_title(name, group)
        row, col = i // 2, i % 2
        a1 = axes[row, col]
        a2 = a1.twinx()
        # group.plot.hist(ax=a2, bins=c.BINS, alpha=.3, xlim=c.XLIM, grid=True, figsize=c.FIGSIZE, xticks=xticks)
        plt.axvline(x=-5, color='black', alpha=0.5)
        plt.axvline(x=-3, color='black', alpha=0.5)
        plt.axvline(x=0)
        plt.axvline(x=15)
        group.plot.kde(bw_method=c.BW_METHOD,
                       title=title,
                       ax=a1,
                       c='r',
                       xlim=c.XLIM,
                       figsize=c.FIGSIZE)
        group.plot.hist(cumulative=True,
                        density=1,
                        bins=c.BINS_CUMULATIVE,
                        range=c.XLIM,
                        ax=a2,
                        alpha=0.3,
                        xticks=xticks,
                        grid=True)
    fig.tight_layout()
    plt.savefig('charts/single/{date}_{city}_{bw_method}.png'.format(date=date, city=city, bw_method=c.BW_METHOD),
                bbox_inches='tight',
                orientation='portrait')

def print_distribution(df, city=None, date=None, tt=None):
    n = len(df)
    df.hist(column=c.EARLINESS_ARIVALL, bins=1000)
    plt.savefig("charts/{date}_{city}_{tt}_{n}.png".format(date=date, city=city, tt=tt, n=n),
                bbox_inches='tight',
                orientation='portrait')

def describe(df, tt=None):
    print('TT = {}. Length = {}'.format(tt, len(df)))
    pp.pprint(df.describe())

def main():
    city = sys.argv[1].lower().capitalize()
    date = sys.argv[2]
    print('Analysing for {} on {}'.format(city, date))

    # con_wh = stuart.db.get_readonly_engine_for_stuart_warehouse()
    con_wh = stuart.db.get_engine_for_stuart_backend()
    db_qs = qs.qs_pu_date_city.format(date=date, e=city)

    rides = pd.read_sql(db_qs, con_wh)
    rides.to_csv('./test.csv')

    compute_kde(rides, date, city)

    #TODO: remove jobs with manual interactions (no pickup_at).


if __name__ == '__main__':
    """
    Analyse the distributions per day per transport type.
    """
    main()