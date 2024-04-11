import json
import os.path
import pandas as pd
from datetime import datetime, timedelta

from create_graphics import word_cloud_with_stopwords
from paths import *

START_DATE_STR = '2018-12-04'
# START_DATE_STR = '2024-04-01'
DATE_FORMAT = '%Y-%m-%d'


def read_day_data(file_path, date):
    fn = f'{file_path}{date}.json'

    if os.path.exists(fn):
        with open(fn) as f:
            return json.load(f)


if __name__ == '__main__':
    today = datetime.now().date()
    current_date = datetime.strptime(START_DATE_STR, DATE_FORMAT).date()
    day_data = read_day_data(FREQUENCY_MAPS_PATH, current_date)

    current_week = current_date.isocalendar().week
    current_month = current_date.month
    current_year = current_date.year

    week_data = []
    month_data = []
    year_data = []
    all_time_data = []

    if day_data:
        week_data.append(day_data)
        month_data.append(day_data)
        year_data.append(day_data)

    while current_date <= today:
        current_date_iso = current_date.isocalendar()
        next_date = current_date + timedelta(days=1)
        day_data = read_day_data(FREQUENCY_MAPS_PATH, next_date)

        # WEEK
        # if current_week == next_date.isocalendar().week:
        #     if day_data:
        #         week_data.append(day_data)
        # else:
        #     df = pd.DataFrame(week_data)
        #     file_name = f'{AGGREGATES_WEEK_PATH}frequency_maps/{current_date.year}_{current_date_iso.week:02d}.json'
        #     with open(file_name, 'w', encoding='utf-8') as of:
        #         df.sum().to_json(of, force_ascii=False)
        #
        #     week_data = []
        #     if day_data:
        #         week_data.append(day_data)
        #     current_week = next_date.isocalendar().week

        # MONTH
        # if current_month == next_date.month:
        #     if day_data:
        #         month_data.append(day_data)
        # else:
        #     df = pd.DataFrame(month_data)
        #     file_name = f'{AGGREGATES_MONTH_PATH}frequency_maps/{current_date.year}_{current_date.month}.json'
        #     with open(file_name, 'w', encoding='utf-8') as of:
        #         df.sum().to_json(of, force_ascii=False)
        #
        #     month_data = []
        #     if day_data:
        #         month_data.append(day_data)
        #     current_month = next_date.month

        # YEAR
        # if current_year == next_date.year:
        #     if day_data:
        #         year_data.append(day_data)
        # else:
        #     df = pd.DataFrame(year_data)
        #     file_name = f'{AGGREGATES_YEAR_PATH}frequency_maps/{current_date.year}.json'
        #     with open(file_name, 'w', encoding='utf-8') as of:
        #         df.sum().to_json(of, force_ascii=False)
        #
        #     year_data = []
        #     if day_data:
        #         year_data.append(day_data)
        #     current_year = next_date.year

        # all_time_data.append(day_data)

        current_date = next_date

    # ALL TIME
    file_name = f'{AGGREGATES_PATH}frequency_maps/all_time_data.json'
    with open(file_name, 'w', encoding='utf-8') as of:
        df = pd.DataFrame(all_time_data)
        df.sum().to_json(of, force_ascii=False)

    # REMAINING DATA
    if len(week_data) > 0:
        pass
    if len(month_data) > 0:
        pass
    if len(year_data) > 0:
        pass