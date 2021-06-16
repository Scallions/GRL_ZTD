"""
Code for data loading and some code about dataset used in ml with torch
"""

import torch
import pandas as pd

import tools


class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

def create_dataset():
    ds = MyDataset(1)

def create_dataloader(ds):
    dataloader = torch.utils.data.DataLoader(dataset=ds,
                                             batch_size=32, shuffle=True, drop_last=True)

def load_datas():
    for fp in tools.tm_files():
        pass

