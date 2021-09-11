import pandas as pd
import numpy as np
from datetime import datetime


def rearran(exc, label=""):
    if label == "짜증":
        value = 0
    elif label == "슬픔":
        value = 1
    elif label == "불안":
        value = 2
    li = []
    for i in range(len(exc)):
        em = exc['해당 내용의 감정 단어'][i].split(",")
        for j in range(len(em)):
            li.append([em[j], value])
    return li


def org_save(columns, li_cl):
    da = pd.DataFrame(columns=columns)
    for i in range(len(li_cl)):
        # print(li_cl[i])
        df = pd.Series(li_cl[i], index=["word", "부정label(0-짜증,1-슬픔,2-해당없음)"])
        da = da.append(df, ignore_index=True)

    da['word'].replace('', np.nan, inplace=True)
    da['word'].replace(' ', np.nan, inplace=True)
    da.dropna(inplace=True)
    print("null 값", da['word'].isnull().sum())
    print("info", da.info())
    da = da.reset_index(drop=True)
    da.to_excel("감정분류파일/new슬픔data.xlsx", index=False)
    data = da.copy()
    print(data)

    for i in range(len(da)):
        data['word'][i] = data['word'][i].lstrip()
        # print(type(data["word"][i]))
        # print(da["word"][i].lstrip())
        if da["word"][i][0] == ' ' and da["word"][i][1] == ' ':
            data.drop(i, inplace=True)
        elif da["word"][i][0] == ' ':
            print(data['word'][i])
            data['word'][i] = data['word'][i][1:]

        else:
            print(data['word'][i])
        if i == len(da) - 1:
            data.to_excel("감정분류파일/new슬픔data.xlsx")
    print(data)
    return data


def concat_space_remove(dat, da):
    csv = pd.concat([dat, da])
    print("데이터 합치기")
    csv['word'].replace('', np.nan, inplace=True)
    csv['word'].replace(' ', np.nan, inplace=True)
    csv.dropna(subset=['word'], inplace=True)
    print(csv['word'].isnull().sum())
    print(csv.info())

    csv.drop_duplicates(['word'], keep='first', inplace=True)
    csv.dropna(subset=['word'], inplace=True)
    csv = csv.reset_index(drop=True)

    remove_shortword(csv, "슬픔data")


def duplicate_and_reset(ex, name=""):
    ex.drop_duplicates(['word'], keep='first', inplace=True)
    ex.dropna(subset=['word'], inplace=True)
    ex = ex.reset_index(drop=True)
    d = datetime.now()
    if name == "":
        ex.to_excel('감정분류파일/%02d%02d슬픔.xlsx' % (d.month, d.day), index=False)
    else:
        ex.to_excel(f'감정분류파일/{name}.xlsx', index=True)


def remove_shortword(ex, name=""):
    li = []
    for i in range(len(ex)):
        if len(ex['word'][i]) == 1:
            li.append(i)
    ex = ex.drop(li)
    duplicate_and_reset(ex, name)


if __name__ == '__main__':
    """사전 합치기 및 전처리를 해주는 폴더 """
    ang1 = pd.read_excel('사전작업/불안1.xlsx') #사전이름을 pd.read_excel('')에 넣어주면됨
    ang2 = pd.read_excel('사전작업/분노1.xlsx')
    sad = pd.read_excel('사전작업/슬픔1.xlsx')

    li1 = rearran(ang1, "불안")
    li2 = rearran(ang2, "분노")
    li3 = rearran(sad, "슬픔")
    #
    li_cl = li1 + li2 + li3
    columns = ["word", "부정label(0-짜증,1-슬픔,2-해당없음)"]
    da = org_save(columns, li_cl)
    csv = pd.read_excel('감정분류파일/슬픔data.xlsx')
    concat_space_remove(da, csv)


