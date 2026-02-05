# Week 3 Example — Input + Control Feel

This example supports the Week 3 slides.

## Run
From this folder:

- `python3 -m pip install pygame`
- `python3 main.py`

## Controls
- Arrow keys / WASD: move (top-down)
- `P`: toggle platformer mode (jump + gravity)
- `Up` / `W` / `Space`: jump (platformer mode)
- Press Jump/Up Twice to perform a double jump!
- `Left Shift`: dash (cooldown)
- `1` / `2` / `3` / `4` / `5` : feel preset (tight/floaty/heavy/under water/super tight)
- `C`: cycle control scheme (WASD / arrows / IJKL)
- `F1`: toggle debug overlay
- `Tab`: cycle boundary mode (clamp/wrap/bounce)
- `R`: reset
- `Space`: start (from title)
- `Esc`: quit


## Tuning Log
- Adding control mapping pipeline
  - The original set up had the buttons hard coded into the directions with the pipeline of actions. I created an actions class on lines 20-24 that created the actions of moving up, down, left or right. From there in _scheme_keys. The keys are assigned different actions instead of just being hard coded to be left right. These binds can easily changed and any key can be mapped to any action.
- Adding a double jump as a discrete action.
  - For this I added the two boolean variables:
    - double_jump_requested (to match the similar jump_requested)
      - Denotes that the player has requested for a double jump
    - double_jump_used
      - Ensures the player can't infinitely jump with double jump. It's only a single use
  - created a conditional on lines 222-223 to set double_jump_requested to True if the the player has already jumped and they press a jump key again.
  - Added onto the original jump conditional in update() to allow for the double jump to be activated only after jump has been requested.
  - Added a statement to _apply_platformer_vertical_bounds for when the play touches the ground double_jump_used to False, essentially resetting the double jump ability
- Added feedback to the double jump. When double jump is used the player turns red and then it turns back to blue when it touches the ground. I was inspired by Celeste for this feedback and it simply conveys to the player that the double jump has recharged
  - Added conditionals in draw on line 500 - 506 to change the local varable of "color" based on whether the double_jump_used it True. Else: the color is blue.
- Adding Two new feelPresets
  - Adding the preset of Under Water. This preset has slow acceleration and slow speed to mimic the feeling of movement under water. This mode works best in the top down control scheme.
  - Adding the preset of Super Tight. This preset increases acceleration, max_speed, and friction compared to the tight preset. I am a fan of Metroid Dread which has very quick tight movements and I tried to replicate that with his preset. It works best in the platformer mode. The raised speed and acceleration allow for faster movement and the raised friction allows for faster feeling changes in direction. 

## Scope
The goal for this project was to add different movement feelings. Water levels are some of my favorite in games like super mario and the addition of a water movement pattern with slow movemet makes a player be more careful with their movements as they may not have time to react to something coming their way. On the flip side, when testing the tight control preset I thought it could be tighter. Adding the super tight preset allows the player to make quick concise movements that give the player more direct control of the play when they need to make split second decisions. I added the double jump feature to give the player a more unique way to move around. This implementation can lead to more unique puzzles and challenges around using double jump. Finally I added a mapping layer to the controls so they were not hard coded into certain actions. Any player can assign any keys to the any of the actions in the action class.
