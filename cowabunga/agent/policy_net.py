import torch
import torch.nn as nn


class PolicyNet(nn.Module):
    """Simple policy network."""

    def __init__(self, obs_dim: int, action_dim: int):
        """Instantiates network.
        Args:
            state_dim: dimension of observation from environment.
            action_dim: dimension of action space.
        """
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim),
            nn.Softmax(dim=-1),
        )

    def forward(self, x: torch.Tensor):
        """Forward pass of the network."""
        return self.net(x)
