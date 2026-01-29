# Week 2 Example — Movement + Boundaries

This example supports the Week 2 slides.

## Run The Game
From this folder:

- `python3 -m pip install pygame`
- `python3 main.py`

## Controls
- Arrow keys / WASD: move
- `Tab`: cycle boundary mode
- `Up` / `W`: jump (platformer mode)
- `R`: reset level
- `Space`: start (from title)
- `Esc`: quit

## Tuning Log with specific values

Note: The feedback I recieved from A1 was very clear that you want explicit changes in value that I have made to the code. Unfortunately it's not as simple as changing a few values to achieve the changes I want, so for the explicit changes in this section you will explicitly recieve: what I added, the precise lines where you can find them in the code, and the word for word code/values that has been added. In addition to this you will recieve information on what was removed from the code and the reason for why. There are 6 major bullet points with things that have been added and 2 with things removed. They all have sub bullet points explicitly showing the new values. I am really trying not to get dinged 20% for formatting again, so this will include all explicit changes. If you have any further questions or suggestions on format please let me know.

- Adding the Barriers 
    The idea for the barriers is that they should randomly make it harder for the player to reach the goal
    - Added Barrier Class
        - Line 24-25
            class Barriers:
                rect: pygame.Rect
    - Added self.barrier1 and self.barrier2 with dimensions of with (40, 400) or (400, 40) in init. Those dimensions were chosen so they would be significant but still avoidable.
        - Lines 70-71
            self.barrier1 = Barriers(rect=pygame.Rect(0, 0, 40, 400))
            self.barrier2 = Barriers(rect=pygame.Rect(0, 0, 400, 40))
    - Added drawing the barriers gray in draw()
        - Lines 374-375
            pygame.draw.rect(self.screen, (128, 128, 128), self.barrier1.rect, border_radius=6)
            pygame.draw.rect(self.screen, (128, 128, 128), self.barrier2.rect, border_radius=6)
- Adding rectNoOverlap
    An issue I kept running into was the teleporter and barriers spawning on top of each other, so I implemented this overlap detection using an array of the rects coordinates
    - defined rectNoOverlap
        - Lines 118 - 123
            def rectNoOverlap(self, rect: pygame.Rect, others: list[pygame.Rect], margin: int = 60) -> None:
                while True:
                    p = self._random_point_in_playfield(margin)
                    rect.center = (int(p.x), int(p.y))
                    if not any(rect.colliderect(o) for o in others):
                return
    - added the method to _reset_level so they will randomly place, not on top of each other, every reset.
        - Lines 91-100
            
            self.rectNoOverlap(self.teleporter.rect, placed_rects, margin=70)
            placed_rects.append(self.teleporter.rect) #adds position to place_rects

            
            self.rectNoOverlap(self.barrier1.rect, placed_rects, margin=70)
            placed_rects.append(self.barrier1.rect)

            self.rectNoOverlap(self.barrier2.rect, placed_rects, margin=70)
            placed_rects.append(self.barrier2.rect)

- Adding goalNoOverlap
    Similarly to rectNoOverlap, I was having issues with the goal overlapping, but the goal isnt a rect so I created its own method for not overlapping. It still uses the rect array to know where things are and makes sure not to place on top of those rects
    - defined goalNoOverlap
        - Lines 125-135
            def goalNoOverlap(self, goal: Goal, obstacles: list[pygame.Rect], margin: int = 60) -> None:
                size = goal.radius * 2
                goal_rect = pygame.Rect(0, 0, size, size)

                while True:
                    p = self._random_point_in_playfield(margin)
                    goal_rect.center = (int(p.x), int(p.y))

                    if not any(goal_rect.colliderect(o) for o in obstacles):
                        goal.pos.update(p)
                        return
    - added the method to _reset_level so it will randomly place, not on top of the other objects, every reset.
        - Line 103
            self.goalNoOverlap(self.goal, placed_rects, margin=60)

- Adding rectObjCollision
    Of course adding new objects means I needed to add the collision for those objects. I elected for a clamp, because I think that makes the most sense for barriers. 
    - Defines recObjCollision - clamping the player to the edge of the object and killing its speed.
        - Lines 240-264
            def rectObjCollision(self, player: pygame.Rect, obstacle: pygame.Rect) -> None: #ADDED for the collision with the rectangles
                if not player.colliderect(obstacle):
                    return

                dx_left = player.right - obstacle.left
                dx_right = obstacle.right - player.left
                dy_top = player.bottom - obstacle.top
                dy_bottom = obstacle.bottom - player.top

                min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

                if min_overlap == dx_left:
                    player.right = obstacle.left # Clamps player to the edge of the object
                    self.player_vel.x = 0 #Kills velocity
                elif min_overlap == dx_right:
                    player.left = obstacle.right
                    self.player_vel.x = 0
                elif min_overlap == dy_top:
                    player.bottom = obstacle.top
                    self.player_vel.y = 0
                elif min_overlap == dy_bottom:
                    player.top = obstacle.bottom
                    self.player_vel.y = 0

                self.player_pos.update(player.center)
    - Added the collision to update
        - Lines 312-313

            self.rectObjCollision(self.player_rect, self.barrier1.rect)
            self.rectObjCollision(self.player_rect, self.barrier2.rect)

- Adding the incrementation of time
    For create an increasing sense of urgency and to make higher levels more difficult I added a difficulty ramp where the user has 1 second less time to reach the goal every level
    - Adding When reset key pressed the seconds reset to 30
        - Line 152
            self.TIMER_SECONDS = 30
    - Incrementing seconds in update   
        - Line 317
            self.TIMER_SECONDS -= 1 


- Adding a Victory Screen
    With the time continuing to increment every level, the game can go it 30 rounds before it is impossible. Thus I added a victory screen for the player if they sucessfully reach level 29
    - Created a new end screen in draw
        Lines 384-385
            elif self.state == "finish":
            self._draw_center_message("Congradulations You Have Beaten The Game!", "R: Play Again   Tab: Bounds")
    - Added a conditional statement to update state
        lines 318-319
            if self.level == 29: #Added
                self.state = "finish"

- Removal of the option to switch to toggle platformer mode
    The design of the game does not work as a platformer, it doesn't make sense for the player to have the option to switch them, it also cleans up the code.
    - Removal of Gravity
    - Removal of Jump Speed
    - Removal of P key to change modes
    - Removal of platformer_mode
    - Removal of platformer vertical bounds
    - Removal of platformer from HUD
    - Removal of on_ground

- Removal of Glide Bug in Top Down View
    When testing the game initially there was a bug where the player would glide up and left for about two seconds after the player let go of the button.
    - Added section where if player_vel < 20 the player stops. This removed the bug.
        - Lines 294 - 295
            if self.player_vel.length() < 20:
                self.player_vel.update(0, 0)

## Scope
As the game progresses, each level the time the player has to reach the goal decreases by 1 second. This is to make the player feel a greater sense of urgency as the game goes on. The addition of the barriers as the new world object forces the player to quickly decypher possible paths to reach the goal. The optimum path may include using different boundary options or the teleporter if the goal is completely blocked off by barriers. This adds another layer of depth and thought process for the player as they proceed through the game. 
