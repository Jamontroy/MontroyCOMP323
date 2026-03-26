# Week 10 Assignment Starter — A6 Audio Pass

This starter is meant to be a clean base for A6, not a finished submission.

It already includes:

- a small scenes-based `pygame` app
- a centralized audio helper with safe mixer setup
- generated placeholder tones for `start`, `scan`, and background loops
- a mute toggle and separate music/SFX volume constants
- an explicit cooldown on the scan action so they have one anti-spam example to build from

## Run

From this folder:

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install -r requirements.txt`
- `python main.py`

## Controls

- `WASD` or arrow keys: move
- `Space`: scan pulse
- `M`: mute / unmute
- `Esc`: quit

## Tuning Log

# Audio.py
- Added 6 more sounds to the array self.sounds
    - "collect_node" | Sound to be played when nodes are collected
    - "hazard_collide" | sound to be played when the player collides with the hazard
    - "victory_sound" | Plays in the end scene when win = True
    - "gameover_sound" | Plays in end scene whrn win = False
    - "game_music" | Loops when in the Play scene
    - "menu_music" | Loops in the start screen

    All of these sounds have been sources from pixabay.com a royalty free sound website
- I adjusted the volume values for the sound effects and the background music so it sounds good in game

# Game.py
- Implementing the new sounds into the update events of the game
    - TitleScene
        - self.game.audio.play_loop("menu_music") | plays the menu music in the On_Enter Method
        - Removed the verbage around "TODO" in the text on screen
    - EndScene
        - Added conditional statement on enter to decide whether either the victory or defeat sound is played.
            - if self.won: self.game.audio.play("victory_sound")
            - else: self.game.audio.play("gameover_sound")
        - Removed verbage around "TODO" in text on screen
    - PlayScene
        - On_Enter
            - self.game.audio.play_loop("game_music") | special denotion of loop so it does not stop at the end of the song
        - In update
            - self.game.audio.play("collect_node") | added to the node collision
            - self.game.audio.play("hazard_collide") | added to the hazard collision event
## Scope
- Looking to add sound effects to deepen the player feedback of the playable demo. When the player enters the game they hear the opening menu music, this is a medium beat chill song to get the player ready and excited. When brainstorming for menu music I wanted something similar to NBA JAM in the 90's. Gives the player some excitement before entering the game. When the player enters the game they are met with the upbeat in-game song. This song is supposed to make the player feel excited and engaged in the game. When a player collides with a node you hear an electronic zap/ding with a positive tune to denote that this is a good action. When the player collides with a hazard the player hears a punch sound along with the i-frames given to the player. This sound makes it clear that colliding with a hazard is a negative action that should be avoided. The game has two outcomes, either victory or gameover. For victory the player will hear a quick victory sound, I imagine this as a level clear sound to make the player feel happy, but doesn't overdo it with something like the fanfare in Mario. The gameover sound is glassbreaking. This works with the "signal lost" from colliding with too many hazard. It conveys breaking and is clear that it is a negative outcome. I pulled this idea from the Henry Stickman flash games, where when you fail you hear a glass breaking sound. I could have added game over screen music, but I felt like it could have been overwhelming with three different tracks for Start, Game, and Gameover screens. Replaying the upbeat start screen wouldn't reflect the sad nature of a gameover. I chose to keep it quiet after the gameover noise to leave the player to their thoughts to reflect in a way. There is a mute button for all audio features and there is a cooldown on the sonar sound and function