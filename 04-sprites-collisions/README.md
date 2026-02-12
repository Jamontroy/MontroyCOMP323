# Week 4 Example — Sprites + Collisions

This example supports the Week 4 slides (sprites, groups, hitboxes, and collision responses).

## Run
From this folder:

- `python3 -m pip install pygame`
- `python3 main.py`

## Controls
- Arrow keys / WASD: move
- `F1`: toggle debug (hitboxes)
- `R`: reset
- `Esc`: quit

## Tuning Log

- First change I made was changing the hitboxes on the circles from squares to circle masks, this was for fairness.
    - Line 46 & 128 added "self.radius = (visual_size * 0.9 / 2)" based on the document in sakai
    - For both coin and player, I removed the value of Hitbox_size. It wasn't nescessary as I could use visual_size
    - Line 338 added collided=pygame.sprite.collide_circle to the sprite collision call. Makes sure it collides with the circle hitbox
- Adding a "Key that allows for the player to kill the enemies"
    - Add class unlock key lines 84-115
    - Line 176 initialize the key
    - Add it to reset Lines 201-214
    - Add collision to update lines 352-356
    - Adding a new state to the game loop, when the player does not have a key the state is play_nokey and after its collected its play_key
    - Add to draw lines 415-431
    - Add collision box to debug lines 467-468
- Changing some of the shapes of the objects
    - Changes the shape of the enemies from triangles to standard squares, made the key a diamond
    - Changed the shape and draw values for the square class because the collision box was already a square. Lines 437-438
- Adding Feedback to the key
    - I needed to give the player feedback so they could see that the enemies can now be killed after picking up the key
    - When the key is picked up the enemies color turns from red to green denoting they can be killed.
    - Lines 355 - 366 adds a for loop to change the color of all the hazards to the key collision event.

## Scope Note
The player starts the game and looks around, I wanted to use different colors to convey different messages without saying anything. Enemies are red, key is green, coins are gold, player is blue. From the start the player can tell to stay away from the red enemies and they can collect the coins to increase their score. Then they come across the key, when they pick it up the enemies change color to green, the same as the color of the key, showing that they can kill the enemies now. For fairness to the player, I tweaked the bounding boxes of objects to be as close to their visual size as possible. 