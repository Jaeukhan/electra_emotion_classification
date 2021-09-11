import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification
from tqdm.notebook import tqdm
from utils.decompostion import *



class DataClass():

    def __init__(self, sentence):
        # 일부 값중에 NaN이 있음...

        self.dataset = sentence
        # 중복제거
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-small-v2-discriminator")

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        row = self.dataset.iloc[idx, 0:1].values[0]
        text = row

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

        return input_ids, attention_mask


def test(text, load_data, f_name):
    da = pd.DataFrame(columns=['text'])
    da['text'] = text
    device = torch.device("cuda")
    predict_li = []
    pro_li = []
    # tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-small-v2-discriminator")

    model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-small-v2-discriminator").to(device)

    test_dataset = DataClass(da)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)
    model.load_state_dict(torch.load(load_data))
    model.eval()
    for input_ids_batch, attention_masks_batch in tqdm(test_loader):
        y_pred = model(input_ids_batch.to(device), attention_mask=attention_masks_batch.to(device))[0]
        _, predicted = torch.max(y_pred, 1)
        # pro_li.append(y_pred.tolist())
        predict_li.append(predicted.tolist()[0])
    da['predict_0부정_1긍정'] =predict_li
    # da.to_excel('po_ne_result.xlsx', index=False, encoding='utf-8-sig')
    # print("저장완료")

    po_subword_li = []
    neg_subword_li = []

    po_da = data_li('감정분류파일/0828_긍정사전전처리_V2(라벨링체크).xlsx', 'drop_word')
    neg_da = data_li('감정분류파일/0826_부정사전전처리_V4(라벨링체크).xlsx', 'drop_word')  # 감정분류파일/부정감정사전_수정

    for i in range(len(da.index)):
        if da['predict_0부정_1긍정'][i] == 0:
            text = decompose_str(da['text'][i])
            # print(text)
            li = [da['text'][i], text, i]
            neg_subword_li.append(li)

        elif da['predict_0부정_1긍정'][i] == 1:
            text = decompose_str(da['text'][i])
            li = [da['text'][i], text, i]
            po_subword_li.append(li)


    columns = ["text", "predict_0부정_1긍정", "긍(0-기쁨,1-감사함)부(0-분노,1-슬픔,2-불안)", "word"]


    result_csv(da, columns, po_subword_li, neg_subword_li, po_da, neg_da, f_name=f_name)


if __name__ == '__main__':
    excel_name = "사전작업/감사.xlsx" #엑셀 이름을 입력해주세요.
    save_excel_name = "0828_긍정" # 이 이름으로 엑셀  저장.
    pt_file_name = "electra_827.pt"

    excel = pd.read_excel(excel_name)
    print(excel.columns)
    text = excel['내용 ']
    model_load = "checkpoint/"+ pt_file_name#모델 변경시 수정. checkpoint안에 모델 존재.
    test(text, model_load)

