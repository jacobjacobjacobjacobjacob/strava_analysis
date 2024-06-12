from strava.strava_api import get_strava_activities
from strava.data_processing import clean_strava_data
import pandas as pd


"""
IMPLEMENTATIONS
- WEATHER
- DAY OF WEEK
- HEATMAP
- HR ZONES
- CADENCE?
"""



#COMMIT TO GIT!!!!!!!!!

def get_data():
    raw_data = get_strava_activities()
    clean_data = clean_strava_data(raw_data)
    clean_data["date"] = pd.to_datetime(clean_data["date"])
    return clean_data


def get_year_totals(df, year=None):
    """Fetch the sum of each stat by year or all time"""
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


def get_year_averages(df, year=None):
    """Fetch the average of each stat by year or all time"""
    if year is not None:
        df = df[df["date"].dt.year == year]

    df = df.replace(0, pd.NA)  # Replace NaN with 0

    average_distance = df["distance"].mean()
    average_elevation = df["elevation_gain"].mean()
    average_time = df["elapsed_time"].mean()
    average_heartrate = df["average_heartrate"].mean()
    average_suffer_score = df["suffer_score"].mean()

    return {
        "year": year,
        "average_distance": round(average_distance, 1),
        "average_elevation": round(average_elevation, 1),
        "average_time": round(average_time, 2),
        "average_heartrate": round(average_heartrate, 1),
        "average_suffer_score": round(average_suffer_score, 1),
    }


def get_distance_month(df, year=2024):
    if year is not None:
        df = df[df["date"].dt.year == year]
    monthly_distance = df.groupby(df["date"].dt.month)["distance"].sum()
    monthly_distance = monthly_distance.reindex(range(1, 13), fill_value=0)
    df = pd.DataFrame(
        {"Month": monthly_distance.index, "Total Distance": monthly_distance.values}
    )
    df["Month"] = df["Month"].map(
        {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }
    )
    return df


if __name__ == "__main__":
    # Fetch the clean data
    data = get_data()
    y_tot = get_year_totals(data)
    print(y_tot)
    print(data)
    month_dist  = get_distance_month(data, 2023)
    print(month_dist)