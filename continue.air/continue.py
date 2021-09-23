# -*- encoding=utf8 -*-

from airtest.core.api import *

auto_setup(__file__)

ST.OPDELAY = 0.2
ST.FIND_TIMEOUT_TMP = 0.5
ST.FIND_TIMEOUT = 6

quest_wait = 45
cnt = 0
while True:
    cnt += 1
    if cnt <= 5:
        next_button = exists(Template(r"next.png", threshold=0.7, rgb=True, record_pos=(0.125, 0.223), resolution=(1920, 1080)))

        if next_button:
            sleep(0.5)
            touch(next_button)
            sleep(quest_wait)
            cnt = 0
    else:
        done_button = exists(Template(r"done.png", threshold=0.70, rgb=True, record_pos=(-0.004, 0.217), resolution=(1920, 1080)))
        if done_button:
            sleep(0.5)
            touch(done_button)
            sleep(2)
        again_button = exists(Template(r"try_again.png", threshold=0.70, rgb=True, record_pos=(0.345, 0.245), resolution=(1920, 1080)))
        if again_button:
            sleep(0.5)
            touch(again_button)
            sleep(quest_wait)
        cnt = 0