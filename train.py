import torch
import numpy as np
import torch.nn as nn
from torch.optim import Adam
import pytorch_lightning as pl
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


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
        self.games = np.loadtxt("training_games.out", delimiter=",", dtype=int)

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
        self.fc2 = nn.Linear(9, 9)
        self.fc3 = nn.Linear(9, 2)

    def forward(self, x):
        out = F.relu(self.fc1(x))
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
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
    games = np.loadtxt("testing_games.out", delimiter=",", dtype=int)

    model.eval()
    with torch.no_grad():
        for game in games:
            board = game[:-1]
            outcome = game[-1]

            out = model(torch.Tensor(encode_board(board)))
            prediction = torch.argmax(out).item()
            hits.append(int(prediction == outcome))

    acc = (sum(hits) / len(hits)) * 100
    print("Accuracy {}%".format(acc))


if __name__ == "__main__":

    dataset = SampleDataset()
    dataloader = DataLoader(dataset, batch_size=64)

    model = PLNet()
    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model, dataloader)
    evaluate(model)
