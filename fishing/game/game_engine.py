"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.
"""

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y
import pygame

class GameEngine:
    def __init__(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish(x=100, y=180, speed=2, point_value=10, color=(80, 180, 220)),
            Fish(x=400, y=280, speed=-3, point_value=20, color=(220, 100, 80)),
            Fish(x=250, y=380, speed=4, point_value=30, color=(100, 200, 100)),
        ]
        self.hooked_fish = None
        self.score = 0
        self.round_duration = 30
        self.round_start_time = pygame.time.get_ticks()
        self.round_active = True
        self.time_remaining = 30

    def start_new_round(self):
        self.score = 0
        self.round_start_time = pygame.time.get_ticks()
        self.round_active = True
        self.time_remaining = self.round_duration

        self.hook.y = self.hook.surface_y
        self.hook.state = IDLE
        self.hooked_fish = None

        self.fish_list = [
            Fish(x=100, y=180, speed=2, point_value=10, color=(80, 180, 220)),
            Fish(x=400, y=280, speed=-3, point_value=20, color=(220, 100, 80)),
            Fish(x=250, y=380, speed=4, point_value=30, color=(100, 200, 100)),
        ]
    
    def update(self):
        elapsed = pygame.time.get_ticks() - self.round_start_time
        self.time_remaining = max(
            0, self.round_duration - elapsed // 1000
        )

        if elapsed >= self.round_duration * 1000:
            self.round_active = False
            self.time_remaining = 0

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                if self.round_active:
                    self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        elif self.round_active:
            caught = check_catch(self.hook, self.fish_list)

            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Time: {self.time_remaining}", (10, 30))
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        if not self.round_active:
            renderer.draw_text(surface, font, "Round Over! Press R to restart.", (WIDTH // 2 - 150, HEIGHT // 2), color=(255, 0, 0))
            renderer.draw_text(surface, font, f"Final Score: {self.score}", (WIDTH // 2 - 100, HEIGHT // 2 + 30), color=(255, 0, 0))
