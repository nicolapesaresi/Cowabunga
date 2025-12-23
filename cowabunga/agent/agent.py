import torch
import cowabunga.env.settings as settings
from cowabunga.env.actions import Action
from cowabunga.agent.policy_net import PolicyNet


class Agent:
    """Generic class for reinforcement learning agent."""

    def __init__(self):
        """Instantiates the agent."""
        self.state_dim = 102
        self.action_dim = len(Action)
        self.net = PolicyNet(self.state_dim, self.action_dim)

    def preprocess_state(self, state: dict) -> torch.Tensor:
        """Turns state dictionary into input of neural network."""
        lives = state["lives"] / settings.LIVES
        paddle_x = state["paddle_x"] / settings.WIDTH
        cows_flat = []
        for cx, cy in state["cows"]:
            cows_flat.append(cx)
            cows_flat.append(cy)
        while len(cows_flat) < settings.MAX_COWS_ON_SCREEN * 2:
            cows_flat.append(0.0)  # fake x
            cows_flat.append(0.0)  # fake y

        state_vector = [lives, paddle_x, *cows_flat]
        return torch.tensor(state_vector, dtype=torch.float32)

    def choose_action(self, obs: dict) -> Action:
        """Chooses an action from a provided obs.
        Args:
            obs: observation of the game state.
        Returns:
            selected action at this step.
        """
        x = self.preprocess_state(obs)
        probs = self.net.forward(x)
