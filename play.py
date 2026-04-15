import pygame
import pickle
from game.env import FlappyEnv
from rl.agent import QAgent
from collections import defaultdict
import os

# Initialize pygame
pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 30

# Colors (fallback if images don't load)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Playing")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load assets
def load_assets():
    assets = {}
    
    # Load background
    try:
        assets['bg'] = pygame.image.load("assets/bg.png")
        assets['bg'] = pygame.transform.scale(assets['bg'], (WIDTH, HEIGHT))
        print("✓ Loaded background image")
    except Exception as e:
        print(f"✗ Failed to load background: {e}")
        assets['bg'] = None
    
    # Load bird
    try:
        assets['bird'] = pygame.image.load("assets/bird.png")
        assets['bird'] = pygame.transform.scale(assets['bird'], (34, 24))
        print("✓ Loaded bird image")
    except Exception as e:
        print(f"✗ Failed to load bird: {e}")
        assets['bird'] = None
    
    return assets

# Load assets
assets = load_assets()

def render_game(env, score):
    # Draw background
    if assets['bg']:
        screen.blit(assets['bg'], (0, 0))
    else:
        screen.fill((135, 206, 235))  # Sky blue fallback
    
    # Draw pipes (using simple rectangles since pipe.png might not exist)
    pipe_width = 52
    pipe_gap = 120
    
    pipe_x = env.pipe.x
    gap_y = env.pipe.gap_y
    
    # Top pipe
    pygame.draw.rect(screen, GREEN, 
                   (pipe_x, 0, pipe_width, gap_y - pipe_gap))
    # Bottom pipe
    pygame.draw.rect(screen, GREEN,
                   (pipe_x, gap_y + pipe_gap, pipe_width, HEIGHT - (gap_y + pipe_gap)))
    
    # Draw bird with rotation based on velocity
    if assets['bird']:
        # Rotate bird based on velocity
        bird_rotation = min(25, max(-25, -env.bird.vel * 2))
        rotated_bird = pygame.transform.rotate(assets['bird'], bird_rotation)
        bird_rect = rotated_bird.get_rect(center=(int(env.bird.x) + 17, int(env.bird.y) + 12))
        screen.blit(rotated_bird, bird_rect)
    else:
        # Fallback to circle
        pygame.draw.circle(screen, (255, 255, 0), (int(env.bird.x), int(env.bird.y)), 15)
        pygame.draw.circle(screen, BLACK, (int(env.bird.x) + 5, int(env.bird.y) - 5), 3)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw info
    info_text = font.render("AI Playing - ESC to quit", True, WHITE)
    screen.blit(info_text, (10, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(FPS)

def main():
    env = FlappyEnv(WIDTH, HEIGHT, render=True)
    agent = QAgent()
    
    # Load trained model
    model_path = "models/q_table.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            loaded_q_table = pickle.load(f)
            agent.q_table = defaultdict(lambda: [0.0, 0.0], loaded_q_table)
        print("✓ Loaded trained model")
    else:
        print("✗ No trained model found. Please train first using train.py")
        return
    
    print("\n🎮 AI Playing Flappy Bird!")
    print("Press ESC to quit\n")
    
    running = True
    episode = 0
    
    while running:
        state = env.reset()
        done = False
        
        while not done and running:
            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        done = True
            
            # AI action (eval_mode=True for no exploration)
            action = agent.choose_action(state, eval_mode=True)
            next_state, reward, done = env.step(action)
            state = next_state
            
            # Render the game
            render_game(env, env.score)
        
        if running:
            episode += 1
            print(f"Episode {episode}: Score = {env.score}")
            
            # Wait a bit between episodes
            pygame.time.wait(1000)
    
    pygame.quit()
    print(f"\nGame ended. Final episode score: {env.score}")

if __name__ == "__main__":
    main()