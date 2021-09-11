import pandas as pd
import numpy as np
from datetime import datetime
from utils.utils import *

class TrainData_Structure():
    def __init__(self, path, mode="슬픔"):
        self.exc = pd.read_excel(f"pre/{path}.xlsx")
        self.mode = mode

    def data_classifi(self):
        dat = pd.DataFrame(columns=["id", "document", "label"])
        for i in range(len(self.exc)):
            if self.mode == "부정":  # "짜증":0, "슬픔":1, "불안":2
                j = 0
            else:
                j = 1
            ser = pd.Series([i, self.exc["내용 "][i], j], index=["id", "document", "label"])
            dat = dat.append(ser, ignore_index=True)
        return dat

def concat_save(da1, da2):
    dat = pd.concat([da1, da2], ignore_index=True)
    d = datetime.now()
    dat.to_csv(f"train_data/train_data_{d.month}{d.day}.txt", sep="\t", index=False)


if __name__ == '__main__':

    # 1번째 인자 '파일명', 2번째인자 '긍정'인지 '부정'인지
    d1 = TrainData_Structure("분노1", "부정")
    d2 = TrainData_Structure("분노2", "부정")
    d3 = TrainData_Structure("분노3", "부정")
    d4 = TrainData_Structure("분노4", "부정")
    d5 = TrainData_Structure("분노5", "부정")
    d6 = TrainData_Structure("불안1", "부정")
    d7 = TrainData_Structure("슬픔1", "부정")
    d8 = TrainData_Structure("슬픔2", "부정")
    d9 = TrainData_Structure("슬픔3", "부정")


    df1 = d1.data_classifi()
    df2 = d2.data_classifi()
    df3 = d3.data_classifi()
    df4 = d4.data_classifi()
    df5 = d5.data_classifi()
    df6 = d6.data_classifi()
    df7 = d7.data_classifi()
    df8 = d8.data_classifi()
    df9 = d9.data_classifi()

    dat = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], ignore_index=True)
    dat = reset_and_duplicates(dat)

    train = pd.read_csv("train_data.txt", sep="\t")
    concat_save(train, dat)
