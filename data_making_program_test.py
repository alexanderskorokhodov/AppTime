# pip install pywin32
# pip install psutil

import win32gui
import psutil
import win32process
from time import time, sleep
from datetime import date, timedelta
import sqlite3
from plyer import notification


def get_app_name():
    try:
        return psutil.Process(
            win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]).name()
    except:
        return '\\all'


def get_week_name_by_day(day_name):
    # week name = name of Monday of this week

    return day_name - timedelta(days=day_name.weekday())


def write_week_to_db():
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    if cur.execute(
            f"""SELECT week_name FROM weeks WHERE week_name = '{today_week}'""").fetchone() is None:
        cur.execute(f"""INSERT INTO weeks(week_name) VALUES('{today_week}')""")
        con.commit()
    con.close()


def write_today_day_to_db():
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    if cur.execute(
            f"""SELECT day_name FROM days WHERE day_name = '{today_date}'""").fetchone() is None:
        cur.execute(f"""INSERT INTO days(day_name) VALUES('{today_date}')""")
        con.commit()
    if cur.execute(
            f"""SELECT week_name FROM weeks WHERE day{today_date.weekday() + 1} = '{today_date}'""").fetchone() is None:
        cur.execute(
            f"""UPDATE weeks SET day{today_date.weekday() + 1} = '{today_date}' WHERE week_name = '{get_week_name_by_day(today_date)}'""")
        con.commit()
    con.close()


def write_appdata_to_db():
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    apps_in_db = cur.execute(f"""SELECT app_name FROM app_time WHERE id in 
    (SELECT app_time_id FROM apps_time WHERE day_id = 
    (SELECT id FROM days WHERE day_name = '{today_date}'))""").fetchall()
    write_apps = list(apps_time.keys())
    for i in apps_in_db:
        if i[0] in write_apps:
            cur.execute(f"""UPDATE app_time SET time = time + {apps_time[i[0]]} WHERE id in 
                (SELECT app_time_id FROM apps_time WHERE day_id = 
                (SELECT id FROM days WHERE day_name = '{today_date}')) AND app_name = '{i[0]}'""")
            con.commit()
            if i[0] != '\\all':
                cur.execute(f"""UPDATE app_time SET time = time + {apps_time[i[0]]} WHERE id in 
                (SELECT app_time_id FROM apps_time WHERE day_id = 
                (SELECT id FROM days WHERE day_name = '{today_date}')) AND app_name = '\\all'""")
            con.commit()
            del apps_time[i[0]]
            write_apps.remove(i[0])
    for i in write_apps:
        id = cur.execute('''SELECT id FROM app_time ORDER BY id DESC LIMIT 1''').fetchone()
        if id is None:
            id = 0
        else:
            id = id[0]
        cur.execute(
            f"""INSERT INTO app_time(id, app_name, time) VALUES({id + 1}, '{i}', {apps_time[i]})""")
        cur.execute(f"""INSERT INTO apps_time(app_time_id, day_id) VALUES({id + 1},
        (SELECT id FROM days WHERE day_name = '{today_date}'))""")
        con.commit()
        cur.execute(f"""UPDATE app_time SET time = time + {apps_time[i]} WHERE id in 
                (SELECT app_time_id FROM apps_time WHERE day_id = 
                (SELECT id FROM days WHERE day_name = '{today_date}')) AND app_name = '\\all'""")
        con.commit()
        del apps_time[i]
    con.close()


def load_limits_from_db():
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    limits_items = cur.execute("""SELECT app_name, time FROM limits""").fetchall()
    con.close()
    return {i[0]: i[1] for i in limits_items}


def check_limits(able_notification=True):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    limited_apps = cur.execute(f"""SELECT app_name, time FROM app_time WHERE id in 
        (SELECT app_time_id FROM apps_time WHERE day_id = 
        (SELECT id FROM days WHERE day_name = '{today_date}'))
        AND app_name in 
        ('{"', '".join(limits.keys())}')""").fetchall()
    con.close()
    for i in limited_apps:
        if i[0] in limits_done:
            continue
        if able_notification:
            if i[0] == windowTile:
                if limits[i[0]] <= i[1]:
                    notification.notify(message=f'Вы используете приложение {i[0]} слишком долго',
                                        app_name='App Time',
                                        app_icon=path_to_icon,
                                        title='Вы превысили лимит!')
                    limits_done.append(i[0])
        else:
            if limits[i[0]] <= i[1]:
                limits_done.append(i[0])


path_to_db = '../../Downloads/Telegram Desktop/test_AppTime (3)/AppTime_db.sqlite'  # path to DateBase
path_to_icon = '../../Downloads/Telegram Desktop/test_AppTime (3)/appIcon.ico'  # path to icon of app
path_to_update_limits_file = '../../Downloads/Telegram Desktop/test_AppTime (3)/UpdateLimits.txt'  # if the first line of file is '1',
# then limits updates, on default it is empty file

apps_time = {'\\all': 0}
ignored_apps = []
today_date = date.today()
today_week = get_week_name_by_day(today_date)
write_week_to_db()
write_today_day_to_db()
write_appdata_to_db()
limits = load_limits_from_db()  # dict with limits {'app_name': time}
limits_updated = False
limits_done = []  # list of app that already limited

windowTile = ''
while not windowTile:
    windowTile = get_app_name()
last_time = time()
apps_time[windowTile] = 0
while True:
    sleep(0.5)

    # day_updater
    if date.today() != today_date:
        if today_date.weekday() == 0:
            write_week_to_db()
        write_appdata_to_db()
        today_date = date.today()
        write_today_day_to_db()
        limits_done = []

    # limits_updater
    with open(path_to_update_limits_file, 'r') as update_limits_file:
        if update_limits_file.readline() == '1':
            limits = load_limits_from_db()
            limits_updated = True

    if limits_updated:
        limits_done = []
        check_limits(able_notification=False)
        with open(path_to_update_limits_file, 'w') as update_limits_file:
            limits_updated = False

    # limits_checker
    check_limits()

    # main code
    newWindowTile = get_app_name()
    if newWindowTile != windowTile:
        new_time = time()
        # if windowTile is None or windowTile in ignored_apps:
        #     last_time = new_time
        #     windowTile = newWindowTile
        #     continue
        if windowTile not in apps_time:
            apps_time[windowTile] = 0
        apps_time[windowTile] += new_time - last_time
        last_time = new_time
        windowTile = newWindowTile
        write_appdata_to_db()
    else:
        new_time = time()
        # if windowTile is None or windowTile in ignored_apps:
        #     continue
        if windowTile not in apps_time:
            apps_time[windowTile] = 0
        apps_time[windowTile] += new_time - last_time
        last_time = new_time
        write_appdata_to_db()
