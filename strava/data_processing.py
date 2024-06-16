import pandas as pd
from strava.strava_api import get_strava_activities, get_best_efforts
from datetime import datetime, timedelta
from utils import m_to_km, ms_to_kph, sec_to_h
from strava.data_validation import validate_data

"""
Processing Strava activity data to extract clean and relevant information for cycling activities.
1. Fetch data from the Strava API.
2. Filter by activity type and date.
3. Convert various metrics into more readable formats
4. Compiles the cleaned data into a DataFrame
"""


def filter_activities(data, date_threshold=datetime(2023, 1, 1)):
    """Filter activities based on start date and sport type"""
    filtered_data = []
    for activity in data:
        if activity.get("sport_type") != "Ride":
            continue
        start_date_local = datetime.fromisoformat(
            activity["start_date_local"].replace("Z", "+00:00")
        ).replace(tzinfo=None)
        if start_date_local >= date_threshold:
            filtered_data.append(activity)
    return filtered_data


def convert_formats(activity):
    """Convert formats"""
    activity_converted_formats = activity.copy()
    if "distance" in activity_converted_formats:
        activity_converted_formats["distance"] = round(
            m_to_km(activity_converted_formats["distance"]), 1
        )
    if "moving_time" in activity_converted_formats:
        activity_converted_formats["moving_time"] = round(
            sec_to_h(activity_converted_formats["moving_time"]), 2
        )
    if "elapsed_time" in activity_converted_formats:
        activity_converted_formats["elapsed_time_hours"] = round(
            sec_to_h(activity_converted_formats["elapsed_time"]), 2
        )
    if "average_speed" in activity_converted_formats:
        activity_converted_formats["average_speed"] = round(
            ms_to_kph(activity_converted_formats["average_speed"]), 1
        )
    if "max_speed" in activity_converted_formats:
        activity_converted_formats["max_speed"] = round(
            ms_to_kph(activity_converted_formats["max_speed"]), 1
        )

    return activity_converted_formats


def extract_data(activity):
    """Extract required data from activity"""
    start_date_local = datetime.fromisoformat(
        activity["start_date_local"].replace("Z", "+00:00")
    )

    # Calculate end_time using the original elapsed_time in seconds
    end_time = (
        start_date_local + timedelta(seconds=activity.get("elapsed_time", 0))
    ).strftime("%H:%M")

    extracted_data = {
        "date": start_date_local.strftime("%Y-%m-%d"),
        "start_time": start_date_local.strftime("%H:%M"),
        "end_time": end_time,
        "type": "indoor" if activity.get("gear_id") == "b14008209" else "outdoor",
        "distance": activity.get("distance"),
        "average_speed": activity.get("average_speed"),
        "max_speed": activity.get("max_speed"),
        "average_heartrate": activity.get("average_heartrate"),
        "max_heartrate": activity.get("max_heartrate"),
        "elevation_gain": activity.get("total_elevation_gain"),
        "moving_time": activity.get("moving_time"),
        "elapsed_time": activity.get("elapsed_time_hours"),
        "suffer_score": activity.get("suffer_score"),
    }

    # Remove outdoor rides shorter than 10km

    return extracted_data


def clean_strava_data(data):
    """Clean Strava activities data and return as dataframe"""
    filtered_data = filter_activities(data)
    cleaned_data = [convert_formats(activity) for activity in filtered_data]
    extracted_data = [extract_data(activity) for activity in cleaned_data]

    clean_data = pd.DataFrame(extracted_data)

    # Remove outdoor rides shorter than 10km
    clean_data = clean_data.drop(
        clean_data[
            (clean_data["distance"] < 10) & (clean_data["type"] == "outdoor")
        ].index
    )
    clean_data.fillna(0, inplace=True)

    # Sort by ascending order
    clean_data = clean_data.sort_values(by="date")

    # Validate the dataframe
    validate_data(clean_data)

    return clean_data


def add_cumsum_columns(df):
    """Add cumsum_['col_name'] to the dataframe"""
    columns = ["total_distance", "total_time", "total_elevation", "total_rides"]
    for column in columns:
        if column in df.columns:
            df[f"cumsum_{column}"] = df[column].cumsum()
        else:
            print(f"Warning: Column '{column}' does not exist in the DataFrame.")
    return df




#strava_data = get_strava_activities()
#df = clean_strava_data(strava_data)
#best_efforts = get_best_efforts()
#pd.set_option("display.max_rows", None)
#pd.set_option("display.max_columns", None)
#print(df)
