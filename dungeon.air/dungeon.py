# -*- encoding=utf8 -*-

from airtest.core.api import *

auto_setup(__file__)
using("common.air")
import common


def dungeon(name='Aberrant', times=100):
    common.init()
    dungeon_setting = common.get_setting('Dungeon')
    enter_dungeon(dungeon_setting['Quest'])
    loop_dungeon(dungeon_setting['Attempts'], dungeon_setting['SelectDungeonTeam'])
    common.close()
    return


def enter_dungeon(name):
    common.enter_subquests()
    
    swipe([180, 824], vector=[0.0023, -0.4823])
    sleep(1)
    # TODO: consider use image
    namesMap = {
        'Dynast': [167, 353],
        'Officer': [167, 456],
        'Witch': [155, 564],
        'Aberrant': [184, 660]
    }
    pos = namesMap[name]
    touch(pos)
    sleep(1)
    swipe([1313, 851], vector=[-0.0066, -0.4938])
    sleep(1)
    return


def loop_dungeon(times, select_team=True):
    floor10 = wait(Template(r"10th_floor.png", threshold=0.8, record_pos=(0.116, 0.142), resolution=(1920, 1080)))
    touch(floor10)
    sleep(1)
    common.handle_repeat()
    start = exists(Template(r"start_button.png", record_pos=(0.108, 0.218), resolution=(1920, 1080)))
    if not start:
        return
    if select_team:
        while not exists(Template(r"dungeon_team.png", threshold=0.9, record_pos=(-0.097, -0.157), resolution=(1920, 1080))):
            touch([1794, 542])
            sleep(0.5)
    touch(start)
    common.handle_stamina()
    for i in range(times):
        # TODO: handle freeze and failure
        for j in range(9):
            sleep(50)
            try:
                next = wait(Template(r"next_button.png", record_pos=(0.125, 0.223), resolution=(1920, 1080)), timeout=30)
                touch(next)
            except:
                pass
        sleep(70)
        wait(Template(r"repeat_results_ui.png", record_pos=(-0.001, -0.221), resolution=(1920, 1080)), timeout=60)
        touch(Template(r"done_button.png", record_pos=(-0.004, 0.217), resolution=(1920, 1080)))
        sleep(1)
        if i == times - 1:
            touch(Template(r"all_done_button.png", record_pos=(0.128, 0.246), resolution=(1920, 1080)))
        else:
            touch(Template(r"try_again_button.png", record_pos=(0.345, 0.245), resolution=(1920, 1080)))
    sleep(2)
    return


dungeon()
