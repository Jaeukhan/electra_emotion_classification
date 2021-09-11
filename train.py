import pandas as pd
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW, ElectraModel
from tqdm.notebook import tqdm
import datetime

# from transformers import AutoTokenizer, ElectraModel, ElectraTokenizer, AdamW, ElectraForSequenceClassification

device = torch.device("cuda")
mode = "electra"
train_txt_name = "827.txt"

class NSMCDataset(Dataset):

    def __init__(self, csv_file):
        # 일부 값중에 NaN이 있음...
        self.dataset = pd.read_csv(csv_file, sep='\t').dropna(axis=0)
        # 중복제거
        self.dataset.drop_duplicates(subset=['document'], inplace=True)
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-small-v2-discriminator")

        print(self.dataset.describe())

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        row = self.dataset.iloc[idx, 1:3].values
        text = row[0]
        y = row[1]

        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=256,
            pad_to_max_length=True,
            add_special_tokens=True
        )

        input_ids = inputs['input_ids'][0]
        attention_mask = inputs['attention_mask'][0]

        return input_ids, attention_mask, y

train_dataset = NSMCDataset("train_data/%s"%(train_txt_name))

model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-small-v2-discriminator").to(device)

# 한번 실행해보기
# text, attention_mask, y = train_dataset[0]
# model(text.unsqueeze(0).to(device), attention_mask=attention_mask.unsqueeze(0).to(device))
# model.load_state_dict(torch.load("model.pt"))
# print(model)
epochs = 3
batch_size = 16
optimizer = AdamW(model.parameters(), lr=1e-5)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

losses = []
accuracies = []
d = datetime.datetime.now()

for i in range(epochs):
    total_loss = 0.0
    correct = 0
    total = 0
    batches = 0

    model.train()

    for input_ids_batch, attention_masks_batch, y_batch in tqdm(train_loader):
        optimizer.zero_grad()
        y_batch = y_batch.to(device)
        # print(input_ids_batch.size())
        # print(attention_masks_batch.size())
        y_pred = model(input_ids_batch.to(device), attention_mask=attention_masks_batch.to(device))[0]
        # print(y_pred)
        loss = F.cross_entropy(y_pred, y_batch)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        _, predicted = torch.max(y_pred, 1)
        correct += (predicted == y_batch).sum()
        total += len(y_batch)

        batches += 1
        if batches % 100 == 0:
            print("epochs", i+1,"Batch Loss:", total_loss, "Accuracy:", correct.float() / total)
    torch.save(model.state_dict(), f'checkpoint/{mode}_{d.month}{d.day}.pt')

    losses.append(total_loss)
    accuracies.append(correct.float() / total)
    print("Train Loss:", total_loss, "Accuracy:", correct.float() / total)
    # torch.jit.save(model.state_dict(), f'checkpoint/{mode}_v2_model.pt')
print("losses : ", losses, "\t accuracies : ", accuracies)
torch.save(model.state_dict(), f'checkpoint/{mode}_{d.month}{d.day}.pt')