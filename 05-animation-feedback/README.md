# Week 5 Example — Animation + Feedback

This example supports the Week 5 slides (animation states, dt-driven frame timers, and feedback bundles).

## Run
From this folder:

- `python3 -m pip install pygame`
- `python3 main.py`

## Controls
- Arrow keys / WASD: move
- `Space`: start / restart
- `F1`: toggle debug overlay (hitboxes)
- `R`: reset level
- `1`: toggle flash cue
- `2`: toggle screen shake cue
- `3`: toggle hitstop cue
- `4`: toggle particles cue
- `Esc`: quit

## Tuning Log:
- Changing the coins from pulsing to spinning (Lines: 516 - 540)
    - Altered the existing _make_coin_frames method and removed all code around the pulse.
    - Works by changing the shape from a circle to an ellipse and changing the width of the ellipse to give the illusion of spinning.
    - changed the pygame.draw.circle() to pygame.draw.rect() & pygame.draw.elipse().
    - Added the list of the 7 scales which the width iterates through based on i, its clever because it iterates backwards and then forwards.
- Adding the "Watch Out!" feedback when the player in class
    - When you were talking about feedback in class this week (I know I'm a week late) you stressed that in a lot of games feedback appears as text on the screen, like "reload". Keeping this in mind I think a slash "Watch Out!" Directly conveys to the user that touching the hazards puts them in danger along with the animations.
        - Added warning_timer and warning_text to _init_
        - In _apply_damage, warning_timer is set to 0.5, so it appears for that long on screen
        - In update, added a conditonal loop to decrement warning_timer by dt
        - In Draw, added a conditional based on whether warning_timer is > 0, when that is true it draws the text "Watch Out" on the screen.
- Adding the sound effect to the coin
    - I have been wanting to add sounds to my games for a while and I finally bit the bullet and did it. It was surprisingly easy which was a nice surprise. DISCLAIMER: I did not make this coin sound, I pulled it from a royalty free website to use. Here is the link: https://pixabay.com/sound-effects/film-special-effects-coin-recieved-230517/
        - First I downloaded the sound and added it to the /assets file, which I have provided in the repo
        - In main.py I added pygame.mixer.init() to initialize the mixer to play sound
        - In game.py under _init_ I initalized the file as sfx_coin
        - In the coin collision I added sfx_coin.play() to play the sound effect
- Adding the damage sound effect
    - Similar to the coin, this implementation was quite simple. I downloaded the sound effect from here: https://pixabay.com/sound-effects/film-special-effects-punch-04-383965/ 
        - Added the initialization of the sound effect in _init_ as sfx_damage
        - Added sfx_damage.play in the _apply_damage method to play when the player is hit and is not invincible.

## Scope Note:
When playing through this example for the first time, I felt like the feedback for the enemy was pretty spot on to what I expect from games. When I interacted with the coins they didn't feel like coins rather just yellow dots which could be the dots in pacman or the save points in undertale, it didn't scream coin to me. To better convey to the player that the yellow dots were coins, I added a spinning animation similar to that in which you see in Mario games. Now they are very clearly coins, but something was still missing... that classic coin collect sound. Once added it gives that classic satisfaction ping for the player knowing for sure that they collected it. While I thought the damage feedback was satisfactory, the addition of the coin sound effect made the silence when hitting the hazard all the more loud, I simply added a damage sound effect for hitting the enemy. Now the game sounds cleaner all around. Finally I added a "WATCH OUT!" Splash text when the player is hit. It adds another layer for the player to see that hitting the hazard is a bad thing. All in all I think the feedback and animation I added incredibly enhances the immersiveness of the game.