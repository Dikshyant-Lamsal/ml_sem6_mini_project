import numpy as np
import random
from collections import defaultdict
from typing import List, Tuple
import pickle

class QAgent:
    def __init__(self, alpha: float = 0.15, gamma: float = 0.95, 
                 epsilon_start: float = 1.0, epsilon_min: float = 0.05):
        self.q_table = defaultdict(lambda: [0.0, 0.0])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = 0.9995
        self.experience_buffer = []
        self.buffer_size = 1000
        
    def get_q(self, state: Tuple[int, ...]) -> List[float]:
        return self.q_table[state]
    
    def choose_action(self, state: Tuple[int, ...], eval_mode: bool = False) -> int:
        if not eval_mode and random.random() < self.epsilon:
            return random.choice([0, 1])
        return np.argmax(self.get_q(state))
    
    def update(self, state: Tuple[int, ...], action: int, reward: float, 
               next_state: Tuple[int, ...]) -> None:
        q = self.get_q(state)
        next_q = self.get_q(next_state)
        
        td_target = reward + self.gamma * max(next_q)
        td_error = td_target - q[action]
        q[action] += self.alpha * td_error
        
        self.experience_buffer.append((state, action, reward, next_state))
        if len(self.experience_buffer) > self.buffer_size:
            self.experience_buffer.pop(0)
    
    def experience_replay(self, batch_size: int = 32) -> None:
        if len(self.experience_buffer) < batch_size:
            return
        
        batch = random.sample(self.experience_buffer, batch_size)
        for state, action, reward, next_state in batch:
            q = self.get_q(state)
            next_q = self.get_q(next_state)
            q[action] += self.alpha * (reward + self.gamma * max(next_q) - q[action])
    
    def decay_epsilon(self) -> None:
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def save(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
        print(f"Model saved to {filename}")
    
    def load(self, filename: str) -> None:
        try:
            with open(filename, 'rb') as f:
                self.q_table = defaultdict(lambda: [0.0, 0.0], pickle.load(f))
            print(f"Model loaded from {filename}")
        except FileNotFoundError:
            print(f"No saved model found at {filename}")
    
    def decay(self):  # Alias for backward compatibility
        self.decay_epsilon()