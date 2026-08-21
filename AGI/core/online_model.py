# AGI/core/online_model.py

import torch
import torch.nn as nn
import torch.optim as optim

class SimpleBrainNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

    def forward(self, x):
        return self.net(x)


class OnlineLearner:
    def __init__(self):
        self.model = SimpleBrainNet()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def train_step(self, x, target):
        pred = self.model(x)
        loss = self.loss_fn(pred, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()