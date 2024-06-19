import torch.nn as nn
import torch
class SASRec(nn.Module):
    def __init__(self, num_items, embed_dim, num_heads, num_layers):
        super(SASRec, self).__init__()
        self.positive_item_embedding = nn.Embedding(num_items + 1, embed_dim)
        self.negative_item_embedding = nn.Embedding(num_items + 1, embed_dim)
        self.position_embedding = nn.Embedding(32, embed_dim)  # Максимальная длина последовательности - 50
        self.transformer_blocks = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads),
            num_layers=num_layers
        )
        self.fc1 = nn.Linear(embed_dim, 256)  # Учитываем паддинг
        self.relu = nn.LeakyReLU(0.1)
        self.fc2 = nn.Linear(256, num_items + 1)  # Учитываем паддинг

    def forward(self, x, y): #banned_heroes):
        positions = torch.arange(0, x.size(1)).unsqueeze(0).to(x.device)
        x = self.positive_item_embedding(x) + self.negative_item_embedding(y) + self.position_embedding(positions)
        x = self.transformer_blocks(x)
        x = x.mean(dim=1)#torch.mean(x, dim=1).values  # Пулинг по времени
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        # Маскирование забаненных персонажей
        #for banned in banned_heroes:
        #    x[:, banned] = -1
        return x
