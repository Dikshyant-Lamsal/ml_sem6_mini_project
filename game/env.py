from game.bird import Bird
from game.pipe import Pipe
from typing import Tuple

class FlappyEnv:
    def __init__(self, width: int, height: int, render: bool = False):
        self.width = width
        self.height = height
        self.render = render
        self.max_score = 0
        self.reset()

    def reset(self) -> Tuple[int, ...]:
        self.bird = Bird()
        self.pipe = Pipe(self.width, self.height)
        self.score = 0
        self.frames_since_last_pipe = 0
        return self.get_state()

    def get_state(self) -> Tuple[int, ...]:
        return (
            min(15, int(self.bird.y / (self.height / 16))),
            min(15, max(0, int((self.pipe.gap_y - self.bird.y) / 10) + 8)),
            min(15, max(0, int(self.pipe.x / 10))),
            min(7, max(0, int(self.bird.vel / 3) + 4)),
            min(3, self.frames_since_last_pipe // 10)
        )

    def step(self, action: int) -> Tuple[Tuple[int, ...], float, bool]:
        self.bird.update(action)
        self.pipe.update()
        self.frames_since_last_pipe += 1
        
        done = False
        reward = 0.05
        
        distance_to_gap = abs(self.bird.y - self.pipe.gap_y)
        if distance_to_gap < 50:
            reward += 2.0 * (1.0 - (distance_to_gap / 50) ** 2)
        else:
            reward -= 0.02
        
        reward -= abs(self.bird.vel) * 0.01
        
        if self.pipe.collide(self.bird):
            return self.get_state(), -20.0, True
        
        if self.bird.y <= 0 or self.bird.y >= self.height:
            return self.get_state(), -20.0, True
        
        if not self.pipe.passed and self.pipe.x + self.pipe.width < self.bird.x:
            self.pipe.passed = True
            self.score += 1
            self.frames_since_last_pipe = 0
            reward += 25.0
            
            if distance_to_gap < 30:
                reward += 5.0
        
        # Spawn new pipe - removed gap_size parameter
        if self.pipe.x < -self.pipe.width:
            self.pipe = Pipe(self.width, self.height)  # Just use default Pipe
        
        if self.score > self.max_score:
            self.max_score = self.score
            reward += 10.0
        
        return self.get_state(), reward, done