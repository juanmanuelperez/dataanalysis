### Description

There are two main script that can be executed from the CLI in order to generate the plots. Refer to the confluence page [Send Drivers On Time project](https://stuart-team.atlassian.net/wiki/spaces/Disco/pages/775487707/Send+drivers+on+time)

### `main_single`

The command to run the script is as follows:

```bash
python main_single.py Barcelona 2019-02-15
```

It is only possible to run it for:

- one single city
- one specific date

Make sure to always provide the city and then the date. The plot obtained is:

![Barcelona 2019-02-15](https://github.com/juanmanuelperez/dataanalysis/blob/master/sendDriversOnTime/charts/single/2019-02-15_Barcelona_0.5.png)

### `main_multiple`

```bash
python main_multiple.py do Liverpool bike 2019-03-01 2019-02-22 2019-02-15
```

It is only possible to run it for:

- (required) the job type for which the analysis as to be made, e.g. `do`. The other accepted value is `pu`
- (required) one single city or client, e.g. `Barcelona` or `104006`
- (required) define the plot type, e.g. `kde` or `hist`
- (required) one transport type, e.g. `bike`
- (required) as many dates as desired, e.g. `2019-03-01 2019-02-22 2019-02-15`. If only two dates are given, then the system considers it a range and plots the distribution for every date.

The order in which the parameters is very important (city - TT - dates). The plot obtained is:

![Barcelona bike 2019-03-01 2019-02-22 2019-02-15](https://github.com/juanmanuelperez/dataanalysis/blob/master/sendDriversOnTime/charts/multiple_dist/2019-03-04T130536_dist_Barcelona_bike_0.5.png)
