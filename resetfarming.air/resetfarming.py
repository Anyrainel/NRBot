# -*- encoding=utf8 -*-

from airtest.core.api import *
from datetime import datetime

auto_setup(__file__)
using("common.air")
import common


def resetfarm():
    common.init()
    common.enter_dark_memory()
    reset_setting = common.get_setting("ResetFarming")
    loop_reset(reset_setting['Quests'], reset_setting['SaveScreenshot'],
               reset_setting['MaxAttempts'], reset_setting['SelectResetTeam'])
    common.close()
    return


def loop_reset(quests, save_screenshot=True, max_attempts=100, select_team=True):
    for name in common.dark_char_list():
        if name not in quests:
            continue
        touch(common.dark_char(name))
        sleep(2)
        for diff in quests[name]:
            retry = True
            while retry:
                retry = False
                try:
                    loop(max_attempts, diff, save_screenshot, select_team)
                except:
                    retry = handle_exception(name, diff, save_screenshot)
        sleep(2)
        common.back()
    return


def loop(max_attempts=100, difficulty="easy", save_screenshot=True, select_team=True):
    quest = exists(common.difficulty(difficulty))
    if not quest:
        return
    sleep(0.5)
    touch(quest)
    sleep(2)
    if not exists(Template(r"start_button.png", record_pos=(0.109, 0.217), resolution=(1920, 1080))):
        return
    if select_team:
        while not exists(Template(r"reset_team.png", threshold=0.9, record_pos=(-0.117, -0.158), resolution=(1920, 1080))):
            touch([691, 539])
            sleep(0.5)

    for run_num in range(max_attempts):
        sleep(1)
        if run_num > 0:
            touch(quest)
        sleep(1)
        touch(Template(r"start_button.png", record_pos=(0.109, 0.217), resolution=(1920, 1080)))
        sleep(1)
        common.handle_stamina()
        result = wait_fight(difficulty, save_screenshot)
        if result:
            break
    return


def wait_fight(difficulty, save_screenshot):
    sleep(20)
    # wait(Template(r"boss_ui.png", threshold=0.8, record_pos=(-0.446, -0.218), resolution=(1920, 1080)), timeout=120, interval=0.5)
    wait(Template(r"wave_3.png", threshold=0.95, record_pos=(0.47, -0.223), resolution=(1920, 1080)), timeout=120, interval=0.5)
    sleep(3)
    touch(Template(r"pause_ui.png", threshold=0.7, rgb=False, record_pos=(0.467, -0.264), resolution=(1920, 1080)))
    sleep(0.5)
    # requires a fast ST.FIND_TIMEOUT_TMP (e.g. 1 sec) to not risk ending the fight
    success = False
    for _ in range(5):
        if not exists(Template(r"menu_ui.png", record_pos=(0.001, -0.223), resolution=(1920, 1080))):
            touch(Template(r"pause_ui.png", threshold=0.7, rgb=False, record_pos=(0.467, -0.264), resolution=(1920, 1080)))
            sleep(0.5)
        else:
            success = True
            break
    if not success:
        raise Exception("Cannot pause the fight.")
    sleep(1)

    # exists(Template(r"x1_number.png", record_pos=(0.2, -0.137), resolution=(1920, 1080)))
    # exists(Template(r"x1_icon.png", record_pos=(0.151, -0.138), resolution=(1920, 1080)))
    # exists(Template(r"x1_horizontal.png", record_pos=(0.216, -0.135), resolution=(1920, 1080)))
    # exists(Template(r"x1_vertical.png", record_pos=(0.207, -0.136), resolution=(1920, 1080)))
    # exists(Template(r"x0_icon.png", record_pos=(0.15, -0.137), resolution=(1920, 1080)))
    success = False
    if exists(Template(r"x0_number.png", threshold=0.9, record_pos=(0.201, -0.138), resolution=(1920, 1080))) and exists(Template(r"x0_vertical.png", threshold=0.9, record_pos=(0.211, -0.136), resolution=(1920, 1080))) and exists(Template(r"x0_horizontal.png", threshold=0.9, record_pos=(0.223, -0.137), resolution=(1920, 1080))):
        if save_screenshot:
            common.take_screenshot(difficulty + "_quit")
        touch(Template(r"quit_button.png", record_pos=(0.001, 0.168), resolution=(1920, 1080)))
        sleep(1)
        touch(Template(r"ok_button.png", record_pos=(0.108, 0.152), resolution=(1920, 1080)))
        sleep(10)
    else:
        if save_screenshot:
            common.take_screenshot(difficulty + "_pass")
        touch(Template(r"back_button.png", record_pos=(-0.002, 0.212), resolution=(1920, 1080)))
        sleep(10)
        done = wait(Template(r"done_button.png", record_pos=(0.344, 0.245), resolution=(1920, 1080)), timeout=120, interval=1)
        if save_screenshot:
            common.take_screenshot(difficulty + "_result")
        sleep(1)
        touch(done)
        sleep(15)
        success = True
    wait(Template(r"subquests_ui.png", threshold=0.85, record_pos=(-0.353, -0.248), resolution=(1920, 1080)), timeout=30, interval=1)
    sleep(1)
    return success


def handle_exception(name, difficulty, save_screenshot):
    for _ in range(6):
        sleep(5)
        done = exists(Template(r"done_button.png", threshold=0.85, record_pos=(0.344, 0.245), resolution=(1920, 1080)))
        if done:
            touch(done)
            sleep(5)
            return False
    resumed = common.restart_app(resume=True)
    if resumed:
        result = wait_fight(difficulty, save_screenshot)
        return not result
    else:
        common.enter_dark_memory()
        touch(common.dark_char(name))
        sleep(2)
        return True


resetfarm()
