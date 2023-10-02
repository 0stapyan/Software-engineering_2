from datetime import datetime, timedelta
import requests
import pytz

timezone = pytz.timezone("Europe/Kyiv")

def fetch_user_data(offset):
    api_url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('data', [])
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None

def format_last_seen(last_seen):

    current_time = datetime.now(timezone)
    last_seen = last_seen.split(".")[0]
    last_time_online = datetime.fromisoformat(last_seen)
    last_time_online = last_time_online.replace(tzinfo=pytz.UTC)
    last_time_online = last_time_online.astimezone(timezone)
    time = current_time - last_time_online

    if time <= timedelta(seconds=30):
        return "just now"
    elif time <= timedelta(minutes=1):
        return "less than a minute ago"
    elif time <= timedelta(minutes=60):
        return "a couple of minutes ago"
    elif time <= timedelta(minutes=120):
        return "an hour ago"
    elif time <= timedelta(hours=24):
        return "today"
    elif time <= timedelta(hours=48):
        return "yesterday"
    elif time <= timedelta(days=7):
        return "this week"
    else:
        return "a long time ago"

def localized_last_seen():
    pass

def get_user_data():
    offset = 0
    user_data = []

    while True:
        users = fetch_user_data(offset)

        if not users:
            break

        user_data.extend(users)
        offset += len(users)

    return user_data

user_data = get_user_data()

for user in user_data:
    username = user.get('nickname', 'unknown user')
    last_seen = user.get('lastSeenDate', None)
    if last_seen:
        time_of_visit = format_last_seen(last_seen)
        print(f"{username} was online {time_of_visit}")
    else:
        print(f"{username} now online")


