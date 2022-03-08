import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq


def create_date_filter(duration_filter, end_date, date_format="%Y-%m-%d"):
    end_date = datetime.datetime.strptime(end_date, date_format)
    end_date = end_date.date()
    start_date = end_date + relativedelta(months=-duration_filter)
    time_filter = str(start_date) + " " + str(end_date)
    return time_filter


def download_google_trends(gt_date_filter, list_keywords):
    # Configure quasi-API
    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)

    pytrends.build_payload(kw_list=list_keywords, cat=71, timeframe=gt_date_filter, geo="NL")

    # Download time-series
    pdf_temp = None
    pdf_temp = pytrends.interest_over_time()

    pdf_temp.reset_index(inplace=True)
    pdf_temp = pdf_temp.reset_index(drop=True)
    # Recast date field into string
    pdf_temp["date"] = pdf_temp["date"].astype(str).str[:10]
    # Reshape the dataframe into long format
    pdf_temp_long = pd.melt(
        pdf_temp,
        id_vars=["date", "isPartial"],
        value_vars=list_keywords,
        var_name=None,
        value_name="value",
        col_level=None,
    )
    pdf_searches = pdf_temp_long.rename(columns={"variable": "keyword", "value": "interest"})

    pdf_searches = pdf_searches.set_index("date")
    return pdf_searches


def create_test_data(keyword):
    google_trends_pdf = download_google_trends(create_date_filter(36, "2020-12-31"), list_keywords=[keyword])
    google_trends_pdf = google_trends_pdf.sort_index()
    timeseries_test = google_trends_pdf[["interest"]]
    timeseries_test = timeseries_test.rename(columns={"interest": "searches"})
    timeseries_test = timeseries_test.reset_index(drop=False)
    timeseries_test["date"] = timeseries_test["date"].astype("datetime64[ns]")
    return timeseries_test


def set_columns_type(df, list_columns, data_type):
    df[list_columns] = df[list_columns].astype(data_type)
    return df


def get_weather_data():
    date_col = "YYYYMMDD"
    pdf_weather = pd.read_csv("./data/weather.csv", sep=";", parse_dates=[date_col])
    pdf_weather = pdf_weather.loc[pdf_weather.loc[:, date_col] >= datetime.datetime(2018, 1, 1)]
    # NG=Mean daily cloud cover (in octants, 9=sky invisible)
    # TG=Daily mean temperature in (0.1 degrees Celsius)
    # SQ=Sunshine duration (in 0.1 hour) calculated from global radiation
    pdf_weather = pdf_weather[[date_col, "NG", "TG", "SQ"]]

    pdf_weather["daily_avg_temperature"] = pdf_weather["TG"] / 10
    pdf_weather = set_columns_type(pdf_weather, ["SQ"], "float64")
    pdf_weather["duration_sunshine"] = pdf_weather["SQ"] / 10
    pdf_weather = pdf_weather.rename(columns={"NG": "daily_avg_cloudiness", "YYYYMMDD": "date"})
    pdf_weather = pdf_weather.set_index("date")
    pdf_weather = pdf_weather.resample("W").agg(
        {
            "daily_avg_temperature": np.mean,
            "duration_sunshine": np.mean,
            "daily_avg_cloudiness": np.mean,
        }
    )

    pdf_weather.reset_index(inplace=True)
    return pdf_weather


def prepare_input_data():
    # time search: 2018 - 2020, aggregation on week level
    pdf_searches = create_test_data("softijs")
    # time weather: 2018 - 2020, aggregation on week level
    pdf_weather = get_weather_data()

    pdf = pd.merge(pdf_searches, pdf_weather, on="date")

    pdf = pdf.loc[pdf.loc[:, "date"] <= datetime.datetime(2020, 6, 1)]
    pdf = pdf.reset_index(drop=True)
    pdf.to_excel("./data/output/data.xlsx")
    return pdf


if __name__ == "__main__":
    pdf = prepare_input_data()
    print(pdf)
