# 🏙️ Beijing Air Quality Dataset

This repository contains historical air quality data from multiple monitoring stations in Beijing, China.

## 📁 Dataset Description

The dataset includes hourly records from 2013 to 2017, with the following features:

- `PM2.5`, `PM10`, `SO2`, `NO2`, `CO`, `O3`
- Meteorological factors: `TEMP`, `PRES`, `DEWP`, `RAIN`, `wd`, `WSPM`
- Timestamp and Station name

## 🗂️ Available Stations

- Aotizhongxin
- Gucheng
- Huairou
- Nongzhanguan
- Shunyi
- Tiantan
- Wanliu
- Wanshouxigong

## 📊 How to Use

You can load the dataset in Python using pandas:

```python
import pandas as pd

url = "https://raw.githubusercontent.com/mhdfrhn13/dataset_airQuality/master/fixData_air_quality.csv"
df = pd.read_csv(url, parse_dates=['datetime'])

## Run steamlit app
```
streamlit run test_app.py
```
