from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

import pygame

class BoundaryMode(str, Enum):
    CLAMP = "clamp"
    WRAP = "wrap"
    BOUNCE = "bounce"

@dataclass
class Goal:
    pos: pygame.Vector2
    radius: int = 16

@dataclass
class Teleporter:
    rect: pygame.Rect

@dataclass  #Added for the random barriers.
class Barriers:
    rect: pygame.Rect

class Game:
    fps = 60

    SCREEN_W, SCREEN_H = 960, 540
    HUD_H = 54
    PLAYFIELD_PADDING = 10

    PLAYER_SIZE = 32
    PLAYER_ACCEL = 2400.0
    PLAYER_MAX_SPEED = 520.0
    PLAYER_FRICTION = 10.0

    TIMER_SECONDS = 30.0

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.font = pygame.font.SysFont(None, 22)
        self.big_font = pygame.font.SysFont(None, 48)

        self.screen_rect = pygame.Rect(0, 0, self.SCREEN_W, self.SCREEN_H)
        self.playfield = pygame.Rect(
            self.PLAYFIELD_PADDING,
            self.HUD_H + self.PLAYFIELD_PADDING,
            self.SCREEN_W - 2 * self.PLAYFIELD_PADDING,
            self.SCREEN_H - self.HUD_H - 2 * self.PLAYFIELD_PADDING,
        )

        self.boundary_mode = BoundaryMode.CLAMP
        self.level = 1
        self.state = "title"  # title | play | win | lose
        self.TopDown_mode = True

        self.player_rect = pygame.Rect(0, 0, self.PLAYER_SIZE, self.PLAYER_SIZE)
        self.player_pos = pygame.Vector2(0, 0)
        self.player_vel = pygame.Vector2(0, 0)

        self.jump_requested = False

        self.time_left = self.TIMER_SECONDS

        self.goal = Goal(pos=pygame.Vector2(0, 0))
        self.teleporter = Teleporter(rect=pygame.Rect(0, 0, 40, 40))

        self.barrier1 = Barriers(rect=pygame.Rect(0, 0, 40, 400)) #Added
        self.barrier2 = Barriers(rect=pygame.Rect(0, 0, 400, 40)) #Added

        self._reset_level(keep_state=True)

    def _random_point_in_playfield(self, margin: int) -> pygame.Vector2:
        x = random.randint(self.playfield.left + margin, self.playfield.right - margin)
        y = random.randint(self.playfield.top + margin, self.playfield.bottom - margin)
        return pygame.Vector2(x, y)

    def _reset_level(self, keep_state: bool = False) -> None:
        self.player_pos = pygame.Vector2(self.playfield.center)
        self.player_vel = pygame.Vector2(0, 0)
        self.player_rect.center = self.player_pos
        self.jump_requested = False

        self.goal.pos = self._random_point_in_playfield(margin=60)

        #Added
        placed_rects: list[pygame.Rect] = [] #an array that holds the positions of the different "rects" on the playscreen. Will be used so objects are not placed on top of each other

        # Teleporter 
        self.rectNoOverlap(self.teleporter.rect, placed_rects, margin=70)
        placed_rects.append(self.teleporter.rect) #adds position to place_rects

        # Barriers
        self.rectNoOverlap(self.barrier1.rect, placed_rects, margin=70)
        placed_rects.append(self.barrier1.rect)

        self.rectNoOverlap(self.barrier2.rect, placed_rects, margin=70)
        placed_rects.append(self.barrier2.rect)

        # Goal
        self.goalNoOverlap(self.goal, placed_rects, margin=60) #Originally I forgot to add the goal since it isn't a rec, but this also uses placed_rects to determine its non overlapping position.



        self.time_left = self.TIMER_SECONDS

        if not keep_state:
            self.state = "play"

    def _cycle_boundary_mode(self) -> None:
        modes = list(BoundaryMode)
        idx = modes.index(self.boundary_mode)
        self.boundary_mode = modes[(idx + 1) % len(modes)]

    #Added
    def rectNoOverlap(self, rect: pygame.Rect, others: list[pygame.Rect], margin: int = 60) -> None:
        while True:
            p = self._random_point_in_playfield(margin)
            rect.center = (int(p.x), int(p.y))
            if not any(rect.colliderect(o) for o in others):
                return

    def goalNoOverlap(self, goal: Goal, obstacles: list[pygame.Rect], margin: int = 60) -> None:
        size = goal.radius * 2
        goal_rect = pygame.Rect(0, 0, size, size)

        while True:
            p = self._random_point_in_playfield(margin)
            goal_rect.center = (int(p.x), int(p.y))

            if not any(goal_rect.colliderect(o) for o in obstacles):
                goal.pos.update(p)
                return

    #---------
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if event.key == pygame.K_TAB:
            self._cycle_boundary_mode()
            return

        if event.key == pygame.K_r:
            self.level = 1
            self.TIMER_SECONDS = 30
            self._reset_level(keep_state=(self.state == "title"))
            if self.state != "title":
                self.state = "play"
            return

        if self.state == "title" and event.key == pygame.K_SPACE:
            self.level = 1
            self.state = "play"
            self._reset_level(keep_state=True)
            return

        if self.state in {"win", "lose"} and event.key == pygame.K_SPACE:
            self.state = "play"
            self._reset_level(keep_state=True)
            return

    def _read_direction(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        x = 0
        y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += 1

        direction = pygame.Vector2(x, y)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        return direction

    def _read_horizontal(self) -> float:
        keys = pygame.key.get_pressed()
        x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += 1
        return float(x)

    def _apply_bounds_player(self) -> None:
        if self.boundary_mode == BoundaryMode.CLAMP:
            self.player_rect.clamp_ip(self.playfield)
            self.player_pos.update(self.player_rect.center)
            return

        if self.boundary_mode == BoundaryMode.WRAP:
            if self.player_rect.right < self.playfield.left:
                self.player_rect.left = self.playfield.right
            elif self.player_rect.left > self.playfield.right:
                self.player_rect.right = self.playfield.left

            if self.player_rect.bottom < self.playfield.top:
                self.player_rect.top = self.playfield.bottom
            elif self.player_rect.top > self.playfield.bottom:
                self.player_rect.bottom = self.playfield.top

            self.player_pos.update(self.player_rect.center)
            return

        # BOUNCE
        bounced = False
        if self.player_rect.left < self.playfield.left:
            self.player_rect.left = self.playfield.left
            self.player_vel.x *= -1
            bounced = True
        elif self.player_rect.right > self.playfield.right:
            self.player_rect.right = self.playfield.right
            self.player_vel.x *= -1
            bounced = True

        if self.player_rect.top < self.playfield.top:
            self.player_rect.top = self.playfield.top
            self.player_vel.y *= -1
            bounced = True
        elif self.player_rect.bottom > self.playfield.bottom:
            self.player_rect.bottom = self.playfield.bottom
            self.player_vel.y *= -1
            bounced = True

        if bounced:
            self.player_pos.update(self.player_rect.center)

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


    def _player_reaches_goal(self) -> bool:
        # Circle-vs-rect (approx): check rect center distance to goal.
        dx = self.player_pos.x - self.goal.pos.x
        dy = self.player_pos.y - self.goal.pos.y
        return (dx * dx + dy * dy) <= (self.goal.radius + self.PLAYER_SIZE * 0.3) ** 2

    def update(self, dt: float) -> None:
        if self.state != "play":
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.state = "lose"
            return

        if self.TopDown_mode:
            direction = self._read_direction()

            # Accelerate toward direction.
            self.player_vel += direction * self.PLAYER_ACCEL * dt

            # Friction:
            if direction.length_squared() == 0:
                self.player_vel -= self.player_vel * min(1.0, self.PLAYER_FRICTION * dt)

            # ADDED Stops the player when the velocity is below 20
            if self.player_vel.length() < 20:
                self.player_vel.update(0, 0)

            if self.player_vel.length() > self.PLAYER_MAX_SPEED:
                self.player_vel.scale_to_length(self.PLAYER_MAX_SPEED)

            self.player_pos += self.player_vel * dt
            self.player_rect.center = (int(self.player_pos.x), int(self.player_pos.y))

            self._apply_bounds_player()

        # Teleporter: collision changes decision (risk/reward positional change).
        if self.player_rect.colliderect(self.teleporter.rect):
            new_pos = self._random_point_in_playfield(margin=80)
            self.player_pos.update(new_pos)
            self.player_rect.center = (int(new_pos.x), int(new_pos.y))

        # Added
        self.rectObjCollision(self.player_rect, self.barrier1.rect)
        self.rectObjCollision(self.player_rect, self.barrier2.rect)

        if self._player_reaches_goal():
            self.level += 1
            self.TIMER_SECONDS -= 1 #Added
            if self.level == 29: #Added
                self.state = "finish"
            else:
                self.state = "win"

    def _draw_hud(self) -> None:
        pygame.draw.rect(self.screen, (46, 52, 64), pygame.Rect(0, 0, self.SCREEN_W, self.HUD_H))

        left = f"Level {self.level}   Bounds: {self.boundary_mode.value.upper()}"
        right = f"Time: {self.time_left:0.1f}s"

        left_surf = self.font.render(left, True, (216, 222, 233))
        right_surf = self.font.render(right, True, (216, 222, 233))

        self.screen.blit(left_surf, (14, 16))
        self.screen.blit(right_surf, (self.SCREEN_W - right_surf.get_width() - 14, 16))

    def _draw_center_message(self, title: str, subtitle: str) -> None:
        title_surf = self.big_font.render(title, True, (236, 239, 244))
        sub_surf = self.font.render(subtitle, True, (216, 222, 233))

        self.screen.blit(
            title_surf,
            (
                self.SCREEN_W // 2 - title_surf.get_width() // 2,
                self.SCREEN_H // 2 - 60,
            ),
        )
        self.screen.blit(
            sub_surf,
            (
                self.SCREEN_W // 2 - sub_surf.get_width() // 2,
                self.SCREEN_H // 2,
            ),
        )

    def draw(self) -> None:
        # Background
        self.screen.fill((20, 24, 30))

        # Playfield
        pygame.draw.rect(self.screen, (10, 12, 16), self.playfield)
        pygame.draw.rect(self.screen, (76, 86, 106), self.playfield, width=2)

        # Goal
        pygame.draw.circle(
            self.screen,
            (163, 190, 140),
            (int(self.goal.pos.x), int(self.goal.pos.y)),
            self.goal.radius,
        )

        # Teleporter
        pygame.draw.rect(self.screen, (180, 142, 173), self.teleporter.rect, border_radius=6)

        # barrier added
        pygame.draw.rect(self.screen, (128, 128, 128), self.barrier1.rect, border_radius=6) #Added
        pygame.draw.rect(self.screen, (128, 128, 128), self.barrier2.rect, border_radius=6) #Added

        # Player
        pygame.draw.rect(self.screen, (136, 192, 208), self.player_rect, border_radius=6)

        self._draw_hud()

        if self.state == "title":
            self._draw_center_message("Week 2", "Space: start   Tab: bounds   Esc: quit")
        elif self.state == "finish":
            self._draw_center_message("Congradulations You Have Beaten The Game!", "R: Play Again   Tab: Bounds") #Added
        elif self.state == "win":
            self._draw_center_message("Level " + str(self.level - 1) +" complete", "Space: next   R: reset   Tab: bounds") #Added
        elif self.state == "lose":
            self._draw_center_message("Time up", "Space: retry   R: reset   Tab: mode")
