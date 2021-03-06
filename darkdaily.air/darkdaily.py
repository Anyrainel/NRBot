# -*- encoding=utf8 -*-

from airtest.core.api import *

auto_setup(__file__)
using("common.air")
import common

def darkdaily():
    common.init()
    common.enter_dark_memory()
    daily_setting = common.get_setting('DarkDaily')
    loop_dark_memory(daily_setting['Quests'], daily_setting['SelectDarkDailyTeam'])
    common.close()
    return


def loop_dark_memory(quests, select_team=True):
    for name in common.dark_char_list():
        if name not in quests:
            continue
        touch(common.dark_char(name))
        sleep(1.5)
        for diff in quests[name]:
            finished = False
            while not finished:
                finished = True
                try:
                    start_daily(diff, select_team)
                except:
                    finished = handle_exception(name)
            select_team = False
        common.back()
        wait(Template(r"subquests_ui.png", threshold=0.85, record_pos=(-0.353, -0.248), resolution=(1920, 1080)), timeout=30, interval=1)
        sleep(1)
    return


def start_daily(diff, select_team=True):
    diff_tpl = common.difficulty(diff)
    touch(diff_tpl)
    sleep(1)
    try:
        start = wait(Template(r"start_button.png", record_pos=(0.108, 0.218), resolution=(1920, 1080)), timeout=3)
    except:
        start = None
    if not start:
        return
    sleep(1)
    if select_team:
        while not exists(Template(r"team_darkdaily.png", threshold=0.93, record_pos=(-0.098, -0.157), resolution=(1920, 1080))):
            touch([692, 542])
            sleep(0.5)
    touch(start)
    common.handle_stamina()
    wait_fight()
    return


def wait_fight():
    sleep(40)
    done = wait(Template(r"done_button.png", record_pos=(0.344, 0.245), resolution=(1920, 1080)), timeout=150, interval=0.5)
    sleep(1)
    touch(done)
    sleep(5)
    wait(Template(r"subquests_ui.png", threshold=0.85, record_pos=(-0.353, -0.248), resolution=(1920, 1080)), timeout=30, interval=1)
    sleep(1)
    return


def handle_exception(name):
    try:
        resumed = common.restart_app(resume=True)
        if resumed:
            wait_fight()
            return True
        else:
            common.enter_dark_memory()
            touch(common.dark_char(name))
            sleep(2)
            return False
    except:
        return handle_exception()


darkdaily()
