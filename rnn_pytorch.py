import torch
import torch.nn as nn


class RNNModel(nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        num_layers: int = 1,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()

        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rnn_out, _ = self.rnn(x)
        last_timestep = rnn_out[:, -1, :]
        return self.fc(last_timestep)


def train_step(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    x_batch: torch.Tensor,
    y_batch: torch.Tensor,
) -> float:
    model.train()
    optimizer.zero_grad()

    predictions = model(x_batch)
    loss = criterion(predictions, y_batch)
    loss.backward()
    optimizer.step()

    return loss.item()


if __name__ == "__main__":
    # Example config + dummy data to verify the scaffold runs.
    input_size = 8
    hidden_size = 32
    output_size = 1
    num_layers = 2
    batch_size = 16
    seq_len = 20

    x = torch.randn(batch_size, seq_len, input_size)
    y = torch.randn(batch_size, output_size)

    model = RNNModel(
        input_size=input_size,
        hidden_size=hidden_size,
        output_size=output_size,
        num_layers=num_layers,
        dropout=0.1,
    )
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    loss = train_step(model, optimizer, criterion, x, y)
    print(f"Startup train step complete. Loss: {loss:.4f}")
