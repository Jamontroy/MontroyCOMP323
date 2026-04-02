# A7 Content Pass Starter

Starting point for Assignment A7 — Content pass + tuning notes.

## How to run

From this folder:

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install -r requirements.txt`
- `python main.py`

## Controls

- Arrow keys: move left/right
- Space: fire
- Escape: quit

## Content map

| Time (sec) | What happens | Difficulty lever | Current value | Assessment |
|---|---|---|---|---|
| 10 sec | First Enemies begin spawning slowly, player gets used to controls and can keep up with shooting them. | SPAWN_DELAY_MS | 800ms | Its a good spawn rate for amble challenge |
| 10sec - 20sec| Enemies start to pile up, the hardest enemies to kill are the fastest ones, player may strategize to focus fast blocks before slow | ENEMY_SPEED_MAX | The enemies are at a proper speed for ample challenge |
| 20sec - 30sec | Player has let a few enemies slip past and has been hit by an enemy | ENEMY_DAMAGE | 20 | Gives the player 5 hits out of their 100 points before they are dead. |
| 30sec - 45sec | A lot of enemies are spawning and the player is not able to kill them fast enough | FIRING_COOLDOWN | 200ms | The cooldown needs to be lowered to make it easier for the player to kill enemies |
| 45sec - 55sec | Player continues to get hit by the enemies as they overwhelm them | PLAYER_HEALTH | 100 | The player health is still at a good rate, the difficulty just ramps up |

## Tuning log

| Variable | Before | After | Why | Result |
|---|---|---|---|---|
| FIRING_COOLDOWN | 200ms | 50ms | I found myself wanting to spam more bullets to make it slightly easier to kill the enemies. Changing this value allows less precise shooting for the player. | Easier shooting experience for the player | 
| PLAYER_SPEED | 5 | 7 | The ability for the player to move faster allows them to kill enemies quicker. I found myself waiting for my player to catch up when Id have to move from one screen to the other. I tested out 10 for speed but I found it too jittery. 7 is a good equalibrium | Result is a smoother player to user connection |
| PROJECTILE_SPEED | -10 | -20 | Gives the player the faster knowledge whether a bullet is going to hit an enemy. I found I needed faster knowledge if my bullets just missed the enemy or hit them and this provides that | Result is the ability for the player to move faster between killing |

## Intended difficulty curve

The difficulty curve starts out low in the easy/boring then heightens up to the good and entertaining when the player is killing blocks but is still challenged by the appearence of new blocks, then moves slightly into unfair and hard as the player begins to be overwhelmed with blocks later in the game. The curve overall may look like a slight curve upwards as the game gets harder as it goes on.