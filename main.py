import requests
import json
from decouple import config

USER_KEY = config('IGDB_KEY')
BASE_URL = "https://api-v3.igdb.com{}"
TIME_TO_BEAT = "/time_to_beats"
GAMES = "/games"
HEADERS = {'user-key': USER_KEY}


def get_game_ids_for_ttb(t):
    payload = """fields *; where completely <= {};""".format(t)
    response = requests.post(BASE_URL.format(TIME_TO_BEAT), headers=HEADERS, data=payload)
    game_json = response.json()
    # game_str = json.dumps(game_json, indent=2)
    game_ids = []
    for g in game_json:
        game_ids.append(g['id'])
    return game_ids


def get_game_hrs(game_id):
    payload = """fields *; where id={};""".format(game_id)
    response = lambda p: requests.post(BASE_URL.format(TIME_TO_BEAT), headers=HEADERS, data=p)
    game_json = response(payload).json()
    hrs = [game_json[0]['completely'], game_json[0]['hastly'], game_json[0]['normally']]
    return max(hrs)


def main():
    ttb = int(input("How many no. of hours per day can you play?\n>>> "))  # time to beat in hours
    # ttb = 0.1
    ttb = 6 if ttb > 6 else ttb
    ttb = 0.1 if ttb < 0.1 else ttb
    ttb = ttb * 30 * 3600  # ttb in seconds
    # print(ttb)
    for game_id in get_game_ids_for_ttb(ttb):
        payload = """fields *; where id={};""".format(game_id)
        response = requests.post(BASE_URL.format(GAMES), headers=HEADERS, data=payload)
        game_data = response.json()
        game_name = game_data[0]['name']
        print(game_name)
        time_to_beat = game_data[0].get('time_to_beat')
        if time_to_beat:
            hrs = get_game_hrs(game_id)
            hrs /= 3600
            print(f"Takes {hrs} hrs to complete")


if __name__ == '__main__':
    main()
