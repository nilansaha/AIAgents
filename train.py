import torch
import numpy as np
import torch.nn as nn
from torch.optim import Adam
import pytorch_lightning as pl
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from tictactoe import TicTacToe
from players import RandomPlayer
from game import Game
import random


def encode_board(board):
    encoded_board_size = len(board) * 2
    encoded_board = np.zeros(encoded_board_size, dtype=int)

    for i, spot in enumerate(board):
        if spot == 0:
            encoded_board[2 * i] = 1
        elif spot == 1:
            encoded_board[2 * i + 1] = 1

    return encoded_board


class SampleDataset(Dataset):
    def __init__(self):
        self.games = np.loadtxt("games_data.out", delimiter=",", dtype=int)

    def __len__(self):
        return len(self.games)

    def __getitem__(self, idx):
        board_state = self.games[idx, 0:-1]
        encoded_board_state = torch.Tensor(encode_board(board_state))
        outcome = torch.tensor(self.games[idx, -1])
        return encoded_board_state, outcome


class PLNet(pl.LightningModule):
    def __init__(self, board_size=3):
        super().__init__()
        self.fc1 = nn.Linear((board_size ** 2) * 2, 9)
        self.fc2 = nn.Linear(9, 2)

    def forward(self, x):
        out = F.relu(self.fc1(x))
        out = self.fc2(out)
        return out

    def training_step(self, batch, batch_idx):
        features, output = batch
        predicted = self(features)
        loss = nn.CrossEntropyLoss()(predicted, output)
        self.log(
            "train_loss", loss, on_epoch=True, on_step=False, prog_bar=True, logger=True
        )
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())

    def on_epoch_start(self):
        print()


def evaluate(model):
    hits = []

    model.eval()
    with torch.no_grad():
        test_case_count = 0
        while True:
            env = TicTacToe(3, 3)
            player1 = RandomPlayer(env)
            player2 = RandomPlayer(env)

            game = Game(env, player1, player2, verbose=False)
            game.play()

            if env.done and env.winner == 0:
                non_winning_state = random.choice(env.state_history[:-1])
                winning_state = env.state_history[-1]

                encoded_non_winning_state = encode_board(non_winning_state)
                out = model(torch.Tensor(encoded_non_winning_state))
                hits.append(int(torch.argmax(out).item() == 0))

                encoded_winning_state = encode_board(winning_state)
                out = model(torch.Tensor(encoded_winning_state))
                hits.append(int(torch.argmax(out).item() == 1))

                test_case_count += 2

            if test_case_count == 200:
                break

    print("Accuracy {}%".format((sum(hits) / len(hits)) * 100))


if __name__ == "__main__":

    dataset = SampleDataset()
    dataloader = DataLoader(dataset, batch_size=64)

    model = PLNet()
    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model, dataloader)
    evaluate(model)
