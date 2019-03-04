#!/usr/bin/env bash

# Running for a specific day and city
python main_analysis.py Paris 2019-02-11
python main_analysis.py Paris 2019-02-12
python main_analysis.py Paris 2019-02-13
python main_analysis.py Paris 2019-02-14
python main_analysis.py Paris 2019-02-15
python main_analysis.py Paris 2019-02-16
python main_analysis.py Paris 2019-02-17
python main_analysis.py Paris 2019-02-18
python main_analysis.py Paris 2019-02-19


# Running the inter comparison
python main_multiple.py Paris bike 2019-02-19 2019-02-18 2019-02-17 2019-02-16 2019-02-15 2019-02-14 2019-02-13 2019-02-12 2019-02-11