from datetime import datetime, timedelta
import requests
import pytz

timezone = pytz.timezone("Europe/Kyiv")

languages = {
        "en": {
            "just now": "just now",
            "less than a minute ago": "less than a minute ago",
            "a couple of minutes ago": "a couple of minutes ago",
            "an hour ago": "an hour ago",
            "today": "today",
            "yesterday": "yesterday",
            "this week": "this week",
            "a long time ago": "a long time ago",
        },
        "es": {
            "just now": "justo ahora",
            "less than a minute ago": "hace menos de un minuto",
            "a couple of minutes ago": "hace un par de minutos",
            "an hour ago": "hace una hora",
            "today": "hoy",
            "yesterday": "ayer",
            "this week": "esta semana",
            "a long time ago": "hace mucho tiempo",
        },
        "ua": {
            "just now": "хвильку тому",
            "less than a minute ago": "менше хвилини тому",
            "a couple of minutes ago": "декілька хвилин тому",
            "an hour ago": "годину тому",
            "today": "сьогодні",
            "yesterday": "вчора",
            "this week": "цього тижня",
            "a long time ago": "дуже давно",
        },
        "fr": {
            "just now": "à l'instant",
            "less than a minute ago": "il y a moins d'une minute",
            "a couple of minutes ago": "il y a quelques minutes",
            "an hour ago": "il y a une heure",
            "today": "aujourd'hui",
            "yesterday": "hier",
            "this week": "cette semaine",
            "a long time ago": "il y a longtemps",
        },
        "it": {
            "just now": "proprio ora",
            "less than a minute ago": "meno di un minuto fa",
            "a couple of minutes ago": "alcuni minuti fa",
            "an hour ago": "un'ora fa",
            "today": "oggi",
            "yesterday": "ieri",
            "this week": "questa settimana",
            "a long time ago": "molto tempo fa",
        },
    }

def fetch_user_data(offset):

    api_url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('data', [])
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None

def format_last_seen(last_seen, lang):

    current_time = datetime.now(timezone)
    last_seen = last_seen.split(".")[0]
    last_time_online = datetime.fromisoformat(last_seen)
    last_time_online = last_time_online.replace(tzinfo=pytz.UTC)
    last_time_online = last_time_online.astimezone(timezone)
    time = current_time - last_time_online

    if time <= timedelta(seconds=30):
        return languages[lang]["just now"]
    elif time <= timedelta(minutes=1):
        return languages[lang]["less than a minute ago"]
    elif time <= timedelta(minutes=60):
        return languages[lang]["a couple of minutes ago"]
    elif time <= timedelta(minutes=120):
        return languages[lang]["an hour ago"]
    elif time <= timedelta(hours=24):
        return languages[lang]["today"]
    elif time <= timedelta(hours=48):
        return languages[lang]["yesterday"]
    elif time <= timedelta(days=7):
        return languages[lang]["this week"]
    else:
        return languages[lang]["a long time ago"]

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

lang = input("Please, choose the language(en, es, ua, fr, it)")

for user in user_data:
    username = user.get('nickname', 'unknown user')
    last_seen = user.get('lastSeenDate', None)

    if last_seen:
        time_of_visit = format_last_seen(last_seen, lang)
        if lang == "en":
             print(f"{username} was online {time_of_visit}")
        elif lang == "es":
             print(f"{username} estis enreta {time_of_visit}")
        elif lang == "ua":
             print(f"{username} був у мережі {time_of_visit}")
        elif lang == "it":
             print(f"{username} era in linea {time_of_visit}")
        elif lang == "fr":
             print(f"{username} était en ligne {time_of_visit}")

    else:
        if lang == "en":
             print(f"{username} now online")
        elif lang == "es":
             print(f"{username} Ahora en línea")
        elif lang == "ua":
              print(f"{username} зараз у мережі")
        elif lang == "it":
              print(f"{username} ora in linea")
        elif lang == "fr":
             print(f"{username} maintenant en ligne")

