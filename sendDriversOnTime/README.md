### Description

There are two main script that can be executed from the CLI in order to generate the plots.

### `main_single`

The command to run the script is as follows:

```bash
python main_single.py Barcelona 2019-02-17
```

It is only possible to run it for:

- one single city
- one specific date

Make sure to always provide the city and then the date.

### `main_multiple`

```bash
python main_multiple.py Liverpool bike 2019-03-01 2019-02-22 2019-02-15
```

It is only possible to run it for:

- one single city, e.g. `Barcelona`
- one transport type, e.g. `bike`
- as many dates as desired, e.g. `2019-03-01 2019-02-22 2019-02-15`

The order in which the parameters is very important (city - TT - dates).
