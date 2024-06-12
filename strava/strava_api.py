from config import (
    strava_client_id,
    strava_athlete_id,
    strava_client_secret,
    strava_refresh_token,
)

import requests

"""
This script retrieves Strava activity data by:
1. Refreshing the Strava API access token using client credentials.
2. Fetching the user's latest activities using the refreshed token.
"""


def get_strava_tokens():
    token_url = "https://www.strava.com/oauth/token"
    refresh_payload = {
        "client_id": strava_client_id,
        "client_secret": strava_client_secret,
        "refresh_token": strava_refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(token_url, data=refresh_payload)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        # new_refresh_token = data.get("refresh_token")

        return access_token
    else:
        print(
            "Error occurred while refreshing token. Status code:", response.status_code
        )
        print(response.text)
        return None


def get_strava_activities():
    access_token = get_strava_tokens()
    if access_token is None:
        raise Exception("Failed to retrieve access token.")

    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"per_page": 200, "page": 1}

    response = requests.get(activities_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data from Strava API: {response.status_code}, {response.text}"
        )

    return response.json()


def get_best_efforts():
    access_token = get_strava_tokens()
    if access_token is None:
        raise Exception("Failed to retrieve access token.")

    athlete_url = f"https://www.strava.com/api/v3/athletes/{strava_athlete_id}/stats"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(athlete_url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data from Strava API: {response.status_code}, {response.text}"
        )

    response = response.json()

    best_efforts = {
        "longest_ride": response["biggest_ride_distance"],
        "biggest_climb": response["biggest_climb_elevation_gain"],
    }

    return best_efforts
