"""
Creation of weekly dispatcher behaviour analysis.

Authors:	Guy Fleury
Date:       2019-02-13
Contact:	g.fleury@stuart.com

"""

import cities
import helper
import pandas as pd
import stuart.db
import matplotlib.pyplot as plt
from matplotlib import ticker as tick

# Set new figure size
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 5
fig_size[1] = 10
# print("Set new figure size:", fig_size)

plt.rcParams["figure.figsize"] = fig_size

# Prints current size
# print("Current figure size:", plt.rcParams["figure.figsize"])

# Indicate main city, year and week to be analysed.
city = input("Specify city: ")

# Check that the inputted city is correct.
if city.lower() not in cities.cities.keys():
    raise ValueError('Value provided ({city}) not authorised.'.format(city=city))

city = city.lower() # To avoid lowering it the following lines.

year = input("Specify year: ")
week = input("Specify week: ")

# Run queries and store into pandas
print("Warehouse query is running...")

con_wh = stuart.db.get_readonly_engine_for_stuart_warehouse()
# with open('queries/SavingsRideTime.txt', 'r') as f:
#     query_textf = f.read().format(query_year=year, query_week=week)
# rides = pd.read_sql(query_textf, con_wh)

country_cities = helper.format_country_cities(cities.cities[city])

# Setup formating of the query
db_querystring = cities.db_querystring[city].format(
    query_year=year,
    query_week=week)

rides = pd.read_sql(db_querystring, con_wh)
print(rides.describe())
helper.save_df(rides, output_path='./data/{city}-Y{year}-W{week}.csv'.format(city=city,
                                                                             year=year,
                                                                             week=week))

# Analyse Accuracy of almost_picking_at vs. pickup_at

# Create figure and subplots
f2, axarr2 = plt.subplots(2)
f2.suptitle('{city} - Week {week}, {year}'.format(city=city, week=week, year=year))

rides[rides.city == city.capitalize()].hist(
    column="almost_picking_at_vs_pickup_at",
    range=(-20, 50),
    bins=1000,
    ax=axarr2[0])

rides[rides.city == city.capitalize()].hist(
    cumulative=True,
    column="almost_picking_at_vs_pickup_at",
    density=1,
    bins=1000,
    range=(-20, 50),
    ax=axarr2[1])

# Set layout for x axes
for x in axarr2:
    x.xaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
    x.set_xlabel("almost_picking vs pickup_at", labelpad=20, weight='bold', size=10)
    x.set_title('')

# Set layout for y axes
axarr2[0].yaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
axarr2[0].set_ylabel("# Jobs", labelpad=20, weight='bold', size=10)

axarr2[1].yaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
axarr2[1].set_ylabel("Cumulative Density", labelpad=20, weight='bold', size=10)

# Save figure 1 as pdf file
f2.savefig("store/{city}_{year}_W{week}.png".format(city=city, week=week, year=year),
           bbox_inches='tight',
           orientation='portrait')

# Rest of FR
# Create figure and subplots

f3, axarr3 = plt.subplots(2)
f3.suptitle('Ro{cc} - Week {week}, {year}'.format(cc=cities.country_codes[city],
                                                  week=week,
                                                  year=year))

rides[rides.city != city.capitalize()].hist(
    column="almost_picking_at_vs_pickup_at",
    range=(-20, 50),
    bins=1000,
    ax=axarr3[0])

rides[rides.city != city.capitalize()].hist(cumulative=True, column="almost_picking_at_vs_pickup_at",
                                            density=1,
                                            bins=1000,
                                            range=(-20, 50), ax=axarr3[1])

# Set layout for x axes
for x in axarr3:
    x.xaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
    x.set_xlabel("almost_picking vs pickup_at", labelpad=20, weight='bold', size=10)
    x.set_title('')

# Set layout for y axes
axarr3[0].yaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
axarr3[0].set_ylabel("# Jobs", labelpad=20, weight='bold', size=10)

axarr3[1].yaxis.set_major_locator(tick.MaxNLocator(nbins=20, steps=(1, 10)))
axarr3[1].set_ylabel("Cumulative Density", labelpad=20, weight='bold', size=10)

# Save figure 1 as png file
f3.savefig("store/Ro{cc}_{year}_W{week}.png".format(cc=cities.country_codes[city],
                                                    week=week,
                                                    year=year),
           bbox_inches='tight',
           orientation='portrait')

# plt.show(block=True)

# end = input("Press Enter")
