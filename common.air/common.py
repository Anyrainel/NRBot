# -*- encoding=utf8 -*-

from airtest.core.api import *
from pathlib import Path
from os import path
import json

def init():
#     ST.PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    ST.OPDELAY = 0.2
    ST.FIND_TIMEOUT_TMP = 1
    ST.FIND_TIMEOUT = 6
    with open(path.join(ST.PROJECT_ROOT, 'settings.jsonc'), 'r') as txt:
        builder = ""
        for linestr in txt.readlines():
            line = linestr.strip()
            if not line.startswith('//'):
                builder += line
        settings = json.loads(builder)
    ST.SETTINGS = settings
    return

def get_setting(entry):
    return ST.SETTINGS['ScriptSettings'][entry]

def get_path(subdir):
    return path.join(ST.PROJECT_ROOT, subdir)

def enter_dark_memory():
    if exists(Template(r"dark_memory_quests.png", record_pos=(-0.391, 0.176), resolution=(1920, 1080))):
        return
    enter_subquests()
    if not exists(Template(r"dark_memory_quests.png", record_pos=(-0.391, 0.176), resolution=(1920, 1080))):
        swipe([180, 824], vector=[0.0023, -0.4823])
        sleep(1)
        touch(Template(r"dark_memory_quest_selected.png", threshold=0.85, record_pos=(-0.394, 0.18), resolution=(1920, 1080)))
        sleep(2)
    return


def enter_subquests():
    touch([1739, 904])
    touch(Template(r"mama_icon.png", record_pos=(0.407, 0.19), resolution=(1920, 1080)))
    sleep(2)
    touch(Template(r"quests_icon.png", target_pos=2, record_pos=(-0.21, 0.177), resolution=(1920, 1080)))
    sleep(2)
    touch(Template(r"subquests_button.png", record_pos=(-0.003, -0.043), resolution=(1920, 1080)))
    sleep(2)
    return


def back():
    touch(Template(r"back_icon.png", record_pos=(-0.471, -0.252), resolution=(1920, 1080)))
    sleep(2)
    return


def close():
    sleep(1)
    touch(Template(r"close_icon.png", record_pos=(
            0.468, -0.25), resolution=(1920, 1080)))
    sleep(1)
    return


def dark_char_list():
    return ["Rion", "Gayle", "Dimos", "Akeha", "Argo", "063y", "F66x", "Lars", "Griff", "Noelle"]


def dark_char(name):
    chars = {
        "Rion": Template(r"rion.png", record_pos=(-0.217, -0.106), resolution=(1920, 1080)),
        "Gayle": Template(r"gayle.png", record_pos=(-0.092, -0.109), resolution=(1920, 1080)),
        "Dimos": Template(r"dimos.png", record_pos=(0.029, -0.11), resolution=(1920, 1080)),
        "Akeha": Template(r"akeha.png", record_pos=(0.155, -0.111), resolution=(1920, 1080)),
        "Argo": Template(r"argo.png", record_pos=(0.28, -0.109), resolution=(1920, 1080)),
        "063y": Template(r"063y.png", record_pos=(0.405, -0.113), resolution=(1920, 1080)),
        "F66x": Template(r"f66x.png", record_pos=(-0.218, 0.176), resolution=(1920, 1080)),
        "Lars": Template(r"lars.png", record_pos=(-0.095, 0.172), resolution=(1920, 1080)),
        "Griff": Template(r"griff.png", record_pos=(0.031, 0.174), resolution=(1920, 1080)),
        "Noelle": Template(r"noelle.png", record_pos=(0.155, 0.176), resolution=(1920, 1080)),
    }
    return chars[name]


def difficulty(name):
    difficulties = {
        "hard": Template(r"dark_lair_hard.png", threshold=0.93, record_pos=(0.139, 0.041), resolution=(1920, 1080)),
        "normal": Template(r"dark_lair_normal.png", threshold=0.93, record_pos=(0.149, -0.059), resolution=(1920, 1080)),
        "easy": Template(r"dark_lair_easy.png", threshold=0.93, record_pos=(0.14, -0.159), resolution=(1920, 1080)),
    }
    return difficulties[name]


def handle_stamina():
    stamina_setting = get_setting('Stamina')
    potions = stamina_setting['RecoveryOrder']
    small_times = stamina_setting['SmallUseTimes'] - 1
    potions_tpl = {
        "small": Template(r"small_stamina_recovery.png", threshold=0.85, record_pos=(-0.012, -0.084), resolution=(1920, 1080)),
        "medium": Template(r"medium_stamina_recovery.png", record_pos=(-0.019, 0.019), resolution=(1920, 1080)),
        "large": Template(r"large_stamina_recovery.png", record_pos=(-0.03, 0.12), resolution=(1920, 1080)),
    }
    if not exists(Template(r"restore_stamina_ui.png", threshold=0.85, record_pos=(-0.001, -0.223), resolution=(1920, 1080))):
        return
    while True:
        swipe([956, 813], vector=[-0.0034, -0.3145])
        sleep(1)
        for potion in potions:
            touch(potions_tpl[potion])
            sleep(1)
            plus = exists(Template(r"plus_button.png", threshold=0.85, record_pos=(0.173, -0.095), resolution=(1920, 1080)))
            if plus:
                if potion == "small":
                    for _ in range(small_times):
                        touch(plus)
                        sleep(0.3)
                break
            else:
                stamina_setting['RecoveryOrder'].remove(potion)
        touch(Template(r"confirm_button.png", threshold=0.8, record_pos=(0.109, 0.217), resolution=(1920, 1080)))
        sleep(0.5)
        touch(Template(r"close_button.png", threshold=0.8, record_pos=(-0.002, 0.151), resolution=(1920, 1080)))
        sleep(2)
        start = exists(Template(r"start_button.png", threshold=0.8, record_pos=(0.109, 0.217), resolution=(1920, 1080)))
        if not start:
            break
        else:
            touch(start)
    return


def handle_repeat():
    if exists(Template(r"loopx10.png", threshold=0.9, record_pos=(-0.34, 0.172), resolution=(1920, 1080))):
        return
    touch(Template(r"gear_icon.png",
          record_pos=(-0.258, 0.172), resolution=(1920, 1080)))
    sleep(1)
    if not exists(Template(r"tick_small.png", threshold=0.8, record_pos=(0.004, 0.024), resolution=(1920, 1080))):
        touch(Template(r"blank_box.png",
              record_pos=(-0.02, 0.023), resolution=(1920, 1080)))
        sleep(0.5)
    swipe(Template(r"slide_icon.png", record_pos=(-0.319, -0.079),
          resolution=(1920, 1080)), vector=[0.1438, 0.0011])
    sleep(0.5)
    touch(Template(r"confirm_button.png", record_pos=(0.106, 0.218), resolution=(1920, 1080)))
    sleep(1)
    return

