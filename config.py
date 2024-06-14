import os
from dotenv import load_dotenv
load_dotenv()


strava_client_id = os.getenv('STRAVA_CLIENT_ID')
strava_client_secret = os.getenv('STRAVA_CLIENT_SECRET')
strava_access_token = os.getenv('STRAVA_ACCESS_TOKEN')
strava_refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
strava_athlete_id = os.getenv('STRAVA_ATHLETE_ID')
