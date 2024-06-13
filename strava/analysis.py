from strava.strava_api import get_strava_activities
from strava.data_processing import clean_strava_data
import pandas as pd


"""
DONE:
- AVERAGE STATS BY YEAR
- TOTAL STATS BY YEAR
- TOTALS SORTED BY MONTH


IMPLEMENTATIONS
- AVERAGE BY MONTH
- WEATHER
- DAY OF WEEK
- HEATMAP
- HR ZONES
- CADENCE?
"""


def fetch_and_clean_strava_data():
    raw_data = get_strava_activities()
    clean_data = clean_strava_data(raw_data)
    clean_data["date"] = pd.to_datetime(clean_data["date"])
    return clean_data


def calculate_yearly_totals(df, year=None):
    """Fetch the sum of each metric by year or all time in a dict"""
    if year is not None:
        df = df[df["date"].dt.year == year]

    total_distance = df["distance"].sum()
    total_elevation = df["elevation_gain"].sum()
    total_time = df["elapsed_time"].sum()
    total_outdoor = df[df["type"] == "outdoor"].shape[0]
    total_indoor = df[df["type"] == "indoor"].shape[0]
    total_rides = total_indoor + total_outdoor
    return {
        "year": year,
        "total_distance": round(total_distance, 1),
        "total_elevation": round(total_elevation, 1),
        "total_time": round(total_time, 2),
        "total_outdoor": total_outdoor,
        "total_indoor": total_indoor,
        "total_rides": total_rides,
    }


def calculate_yearly_averages(df, year=None):
    """Fetch the average of each metric by year or all time in a dict"""
    if year is not None:
        df = df[df["date"].dt.year == year]

    average_distance = df["distance"].mean()
    average_elevation = df["elevation_gain"].mean()
    average_time = df["elapsed_time"].mean()
    average_heartrate = df["average_heartrate"].mean()

    return {
        "year": year,
        "average_distance": round(average_distance, 1),
        "average_elevation": round(average_elevation, 1),
        "average_time": round(average_time, 2),
        "average_heartrate": round(average_heartrate, 1),
    }


def calculate_monthly_metrics(df, year=None):
    """Fetch the sum of each metric in a dataframe sorted by month"""
    df["date"] = pd.to_datetime(df["date"])

    if year is not None:
        df = df[df["date"].dt.year == year]

    monthly_metrics = pd.pivot_table(
        df,
        index=df["date"].dt.month.rename("month"),
        values=["distance", "elevation_gain", "elapsed_time", "type"],
        aggfunc={
            "distance": "sum",
            "elevation_gain": "sum",
            "elapsed_time": "sum",
            "type": "count",
        },
        fill_value=0,
    )

    # Rename columns
    monthly_metrics.rename(
        columns={
            "distance": "total_distance",
            "elevation_gain": "total_elevation",
            "elapsed_time": "total_time",
            "type": "total_rides",
        },
        inplace=True,
    )

    indoor_rides = df[df["type"] == "indoor"]
    outdoor_rides = df[df["type"] == "outdoor"]

    # Calculate counts for indoor and outdoor rides and ensure all months are represented
    indoor_counts = (
        indoor_rides.groupby(indoor_rides["date"].dt.month)
        .size()
        .reindex(range(1, 13), fill_value=0)
    )
    outdoor_counts = (
        outdoor_rides.groupby(outdoor_rides["date"].dt.month)
        .size()
        .reindex(range(1, 13), fill_value=0)
    )

    # Reindex monthly_metrics to ensure all months are included
    monthly_metrics = monthly_metrics.reindex(range(1, 13), fill_value=0)

    monthly_metrics["total_indoor"] = indoor_counts
    monthly_metrics["total_outdoor"] = outdoor_counts

    # Replace NaN values with zeros for total_indoor and total_rides
    monthly_metrics["total_indoor"] = monthly_metrics["total_indoor"].fillna(0)
    monthly_metrics["total_rides"] = (
        monthly_metrics["total_indoor"] + monthly_metrics["total_outdoor"]
    )
    monthly_metrics["total_rides"] = monthly_metrics["total_rides"].fillna(0)

    # Reorder columns
    monthly_metrics = monthly_metrics[
        [
            "total_distance",
            "total_elevation",
            "total_time",
            "total_outdoor",
            "total_indoor",
            "total_rides",
        ]
    ]

    # Map month numbers to month names
    monthly_metrics.index = monthly_metrics.index.map(
        {
            1: "jan",
            2: "feb",
            3: "mar",
            4: "apr",
            5: "may",
            6: "jun",
            7: "jul",
            8: "aug",
            9: "sep",
            10: "oct",
            11: "nov",
            12: "dec",
        }
    )

    return monthly_metrics


if __name__ == "__main__":
    # Fetch the clean data
    data = fetch_and_clean_strava_data()
    #print(data)
    y_tot = calculate_yearly_totals(data, year=2023)
    # print(y_tot)
    month_metric = calculate_monthly_metrics(data, year=2023)
    # pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    # print(data)
    print(month_metric)

    year_avg = calculate_yearly_averages(data, 2023)
    print(year_avg)
