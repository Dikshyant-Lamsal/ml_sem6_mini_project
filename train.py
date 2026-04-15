import pickle
from game.env import FlappyEnv
from rl.agent import QAgent

env = FlappyEnv(400, 600)
agent = QAgent()

EPISODES = 10000

for episode in range(EPISODES):
    state = env.reset()
    total_reward = 0

    while True:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)

        agent.update(state, action, reward, next_state)
        state = next_state
        total_reward += reward

        if done:
            break

    agent.decay_epsilon()  # Changed from decay() to decay_epsilon()

    if episode % 100 == 0:
        print(f"Episode {episode}, Score: {env.score}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.3f}")

# Save trained model
with open("models/q_table.pkl", "wb") as f:
    pickle.dump(dict(agent.q_table), f)  # Convert defaultdict to dict for saving

print("Training complete!")