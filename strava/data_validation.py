import pandas as pd

"""
Functions to validate the data and log errors if they exist.
"""


def check_ride_types(df):
    """Checking the ride types are correct (indoor/outdoor)"""
    errors = []
    for index, row in df.iterrows():
        if (row["type"] == "indoor") and (row["distance"] != 0):
            errors.append(
                f'Error: Indoor ride on {row["date"]} at index {index} has distance value {row["distance"]}.'
            )
        elif (row["type"] == "outdoor") and (row["distance"] == 0):
            errors.append(
                f'Error: Outdoor ride on {row["date"]} at index {index} has no distance value.'
            )
    return errors


def check_data_types(df):
    """Validate data types of columns"""
    errors = []

    # Check data type for 'distance' column
    if not pd.api.types.is_numeric_dtype(df["distance"]):
        errors.append("Error: Distance column must be numeric.")

    # Check data type for 'elevation_gain' column
    if not pd.api.types.is_numeric_dtype(df["elevation_gain"]):
        errors.append("Error: Elevation column must be numeric.")

    # Check data type for 'type' column
    if not pd.api.types.is_string_dtype(df["type"]):
        errors.append("Error: Ride type column must be a string.")

    return errors


def check_missing_values(df):
    """Check for missing values in critical columns"""
    errors = []
    for idx, col in enumerate(["type", "distance", "date"]):
        if df[col].isnull().any():
            errors.append(f"Error: Missing values in column {col} at index {idx}.")
    return errors


def validate_data(df):
    """Run all validation functions and aggregate errors"""
    errors = []

    errors.extend(check_ride_types(df))
    errors.extend(check_missing_values(df))
    errors.extend(check_data_types(df))

    if errors:
        for error in errors:
            print(error)
    else:
        pass
