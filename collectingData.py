# pip install pywin32

import win32gui
import psutil
import win32process
from time import time, sleep
from datetime import date, timedelta
import sqlite3


def get_app_name():
    try:
        return psutil.Process(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]).name()
    except:
        return None


def get_week_name_by_day(day_name):
    # week name = name of Monday of this week

    return day_name - timedelta(days=day_name.weekday())


def write_week_to_bd():
    con = sqlite3.connect("AppTime_db.sqlite")
    cur = con.cursor()
    if cur.execute(f"""SELECT week_name FROM weeks WHERE week_name = '{today_week}'""").fetchone() is None:
        cur.execute(f"""INSERT INTO weeks(week_name) VALUES('{today_week}')""")
        con.commit()
    con.close()


def write_today_day_to_bd():
    con = sqlite3.connect("AppTime_db.sqlite")
    cur = con.cursor()
    if cur.execute(f"""SELECT day_name FROM days WHERE day_name = '{today_date}'""").fetchone() is None:
        cur.execute(f"""INSERT INTO days(day_name) VALUES('{today_date}')""")
        con.commit()
    if cur.execute(
            f"""SELECT week_name FROM weeks WHERE day{today_date.weekday() + 1} = '{today_date}'""").fetchone() is None:
        cur.execute(
            f"""UPDATE weeks SET day{today_date.weekday() + 1} = '{today_date}' WHERE week_name = '{get_week_name_by_day(today_date)}'""")
        con.commit()
    con.close()


def write_appdata_to_bd():
    con = sqlite3.connect("AppTime_db.sqlite")
    cur = con.cursor()
    apps_in_bd = cur.execute(f"""SELECT app_name FROM app_time WHERE id in 
    (SELECT app_time_id FROM apps_time WHERE day_id = 
    (SELECT id FROM days WHERE day_name = '{today_date}'))""").fetchall()
    print(apps_in_bd)
    write_apps = list(apps_time.keys())
    for i in apps_in_bd:
        if i[0] in write_apps:
            cur.execute(f"""UPDATE app_time SET time = time + {apps_time[i[0]]} WHERE id in 
    (SELECT app_time_id FROM apps_time WHERE day_id = 
    (SELECT id FROM days WHERE day_name = '{today_date}')) AND app_name = '{i[0]}'""")
            con.commit()
            del apps_time[i[0]]
            write_apps.remove(i[0])
    for i in write_apps:
        cur.execute(f"""INSERT INTO app_time(app_name, time) VALUES('{i}', {apps_time[i]})""")
        cur.execute(f"""INSERT INTO apps_time(app_time_id, day_id) VALUES(
        (SELECT id FROM app_time WHERE app_name = '{i}'),
        (SELECT id FROM days WHERE day_name = '{today_date}'))""")
        con.commit()
        del apps_time[i]
    con.close()


apps_time = {}
ignored_apps = ['', 'explorer.exe']
today_date = date.today()
today_week = get_week_name_by_day(today_date)
write_week_to_bd()
write_today_day_to_bd()

windowTile = ''
while not windowTile:
    windowTile = get_app_name()
last_time = time()
apps_time[windowTile] = 0
while True:
    sleep(0.5)

    if date.today() != today_date:
        if today_date.weekday() == 0:
            write_week_to_bd()
        write_appdata_to_bd()
        today_date = date.today()
        write_today_day_to_bd()

    newWindowTile = get_app_name()
    if newWindowTile != windowTile:
        new_time = time()
        if windowTile is None or windowTile in ignored_apps:
            last_time = new_time
            windowTile = newWindowTile
            continue
        if windowTile not in apps_time:
            apps_time[windowTile] = 0
        apps_time[windowTile] += new_time - last_time
        last_time = new_time
        windowTile = newWindowTile
        write_appdata_to_bd()
