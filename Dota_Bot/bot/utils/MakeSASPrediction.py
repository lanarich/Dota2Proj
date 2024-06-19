import torch
from SasModel import SASRec

NUM_HEROES = 124
embed_dim = 64
num_heads = 1
num_layers = 1


model = SASRec(NUM_HEROES, embed_dim, num_heads, num_layers)
model.load_state_dict(torch.load('seq_rec_model'))
model.eval()

my_team = torch.tensor([[29, 0, 0, 0]])
enemy_team = torch.tensor([[84, 0, 0, 0]])

pred = model(my_team, enemy_team)

print(torch.topk(pred, 5)[1])