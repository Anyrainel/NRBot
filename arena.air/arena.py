# -*- encoding=utf8 -*-

from airtest.core.api import *

auto_setup(__file__)
using("common.air")
import common


def arena():
    common.init()
    common.enter_arena()
    arena_setting = common.get_setting('Arena')
    for i in range(arena_setting['Attempts']):
        try:
            battle(i, arena_setting['Skills'], arena_setting['Focus'],
                   arena_setting['UseGems'], arena_setting['SaveScreenshot'])
        except:
            handle_exception()
    common.close()
    return


def battle(seed, skills, focus=0, use_gems=True, save_screenshot=True):
    touch(Template(r"battle_button.png", record_pos=(0.339, 0.145), resolution=(1920, 1080)))
    sleep(2)
    wait(Template(r"select_deck_ui.png", record_pos=(-0.088, -0.182), resolution=(1920, 1080)))
    sleep(1)
    opponents = [[388, 334], [390, 549], [395, 736]]
    touch(opponents[seed % 3])
    touch(Template(r"start_button.png", record_pos=(0.109, 0.217), resolution=(1920, 1080)))
    handle_bp(use_gems)
    sleep(10)
    tmp = ST.OPDELAY
    ST.OPDELAY = 0.15
    
    fpos = [None, [70, 132], [90, 293], [78, 446]]
    spos = {
        '1-1': [531, 858],
        '1-2': [631, 946],
        '2-1': [1109, 859],
        '2-2': [1202, 925],
        '3-1': [1698, 850],
        '3-2': [1788, 945],
    }
    while True:
        if focus:
            touch(fpos[focus])
        for _ in range(6):
            for skill in skills:
                touch(spos[skill])
        done = exists(Template(r"done_button.png", record_pos=(0.267, 0.145), resolution=(1920, 1080)))
        if done:
            break
    ST.OPDELAY = tmp
    if save_screenshot:
        won = exists(Template(r"win_rewards.png", record_pos=(0.061, 0.047), resolution=(1920, 1080)))
        common.take_screenshot("win" if won else "lose")
    touch(done)
    sleep(5)
    wait(Template(r"arena_ui.png", threshold=0.85, record_pos=(-0.384, -0.246), resolution=(1920, 1080)), timeout=20, interval=1)
    sleep(3)
    return


def handle_bp(use_gems=True):
    if not exists(Template(r"restore_bp_ui.png", record_pos=(0.002, -0.223), resolution=(1920, 1080))):
        return
    if use_gems:
        touch(Template(r"gems_option.png", record_pos=(-0.076, -0.099), resolution=(1920, 1080)))
        sleep(1)
        touch(Template(r"confirm_button.png", record_pos=(0.109, 0.219), resolution=(1920, 1080)))
        sleep(1)
        touch(Template(r"close_button.png", record_pos=(-0.001, 0.151), resolution=(1920, 1080)))
        sleep(1)
        touch(Template(r"start_button.png", record_pos=(0.109, 0.217), resolution=(1920, 1080)))
        sleep(1)
    else:
        touch(Template(r"close_button.png", record_pos=(-0.001, 0.151), resolution=(1920, 1080)))
        sleep(1)
        touch(Template(r"cancel_button.png", record_pos=(-0.108, 0.217), resolution=(1920, 1080)))
        sleep(1)
        raise Exception("no BP left")
    return


def handle_exception():
    try:
        sleep(3)
        common.restart_app()
        common.enter_arena()
    except:
        handle_exception()
    return


arena()
