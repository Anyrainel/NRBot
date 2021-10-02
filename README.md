# NRBot

NRBot is an image recognition based bot for Nier Reincarnation. NRBot is based on Airtest framework (Python).

It currently only support English UI. Main goal of NRBot is to automate repetitive content in the game where a simple macro won't suffice.

## How to use?

1. Install emulator with adb support (e.g. LDPlayer 64bit). Use 1080x1920 mobile resolution.
2. Turn on adb: Settings -> Other settings -> ADB Debugging -> Open remote connection
3. Install [AirtestIDE](https://airtest.netease.com/). Extract it to your favorite path.
4. Update `settings.jsonc`. Refer to comments for instructions.
5. Make sure you already set up proper team for the quests in game.
6. Run `python NRBot.py <script_name>` in this directory. Here `<script_name>` can be any of the following:
    - `resetfarming`: farms purple grade item in daily dark lairs by resetting if no drop.
    - `darkdaily`: clears all specified daily dark lairs.
    - `dungeon`: farms specified dark dungeon for memoirs.

If you see "device not ready" error, try to run `adb devices` to start the adb daemon.

## Scripts

### `ResetFarming`

**Requirement**: Position the game at Mama's room, or the dark memory quests page.

**Action**: Constantly reset on specified quests and look for purple items. It will try up to the specified attempts for each character and difficulty selected. In settings, you can make the bot save a screenshot for each time when it quits. You can review the screenshots to confirm if the bot is recognizing correctly.

**Note**: After reviewing the screenshots, you can count then discard them by running `python CalcStats.py`. It will accumulate data into `stats.json`. So you can track your progress over time. When you found incorrectly recognized screenshots, you can upload them to issues.

### `DarkDaily`

**Requirement**: Position the game at Mama's room or the dark memory quests page.

**Action**: Loop through all daily dark lair quests. You can specify how many quests (0-3) you have unlocked for each character. The bot will go from top to bottom according to the number, and it will skip if a particular quest has been already cleared.

### `Dungeon`

**Requirement**: Position the game at Mama's room.

**Action**: Loop through specified Dark dungeons to farm memoirs.

## Work in progress

- Detect game crash or freeze.
- Handle failure for dungeon runs.

## Other tips

Some actions can be easily achieved using emulator built-in macro recording. Examples:
1. **Auto repeat any 10x loops**: repeatedly tap the position of the "try again" button at bottom right corner until manual stop or X hours.
2. **Auto sell 2\* and 3\* memmoirs**: record the sell loop (auto or choose 20, then sell) and repeat.
3. **Chapter / event summons**: record the summon loop (try replenish, then summon 100x, wait and hit done) and repeat for X times.

Make sure you have "ASTC Texture" support turned on in your emulator, the game loading screen time would be much longer without it.

FWIW, LDPlayer + high graphics setting gives me the best gameplay smoothness and least crashes (it still happens). You need to adjust the script for longer waiting times if your emulator is too slow.
