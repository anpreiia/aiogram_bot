import sqlite3
import json
import time
import game as game

GAMEDATADB = "gamedata.db"


def player_get(player_id) -> [int, list] or False:
    db = sqlite3.connect(GAMEDATADB)
    cur = db.cursor()

    cur.execute(f"SELECT money, garden FROM players WHERE chat_id = '{player_id}'")
    result = cur.fetchone()
    if result is None:
        db.close()
        return False
    db.close()
    return [result[0], json.loads(result[1])]


def player_create(player_id):
    db = sqlite3.connect(GAMEDATADB)
    cur = db.cursor()

    now = int(time.time())
    g = json.dumps(game.EMPTY_GARDEN)

    cur.execute(f"INSERT INTO players VALUES "
                f"('{player_id}', '{g}', '{game.PLAYER_START_MONEY}', '{now}', '{now}')")

    db.commit()
    db.close()


def player_update(player_id, money, garden):
    db = sqlite3.connect(GAMEDATADB)
    cur = db.cursor()

    now = int(time.time())
    g = json.dumps(garden)

    cur.execute(f"UPDATE players SET garden = '{g}', money = '{money}', last_time_played = '{now}'"
                f"WHERE chat_id = '{player_id}'")

    db.commit()
    db.close()
