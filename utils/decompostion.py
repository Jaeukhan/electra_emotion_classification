import pandas as pd
import numpy as np

cho = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"  # len = 19
jung = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"  # len = 21
jong = "ㄱ/ㄲ/ㄱㅅ/ㄴ/ㄴㅈ/ㄴㅎ/ㄷ/ㄹ/ㄹㄱ/ㄹㅁ/ㄹㅂ/ㄹㅅ/ㄹㅌ/ㄹㅍ/ㄹㅎ/ㅁ/ㅂ/ㅂㅅ/ㅅ/ㅆ/ㅇ/ㅈ/ㅊ/ㅋ/ㅌ/ㅍ/ㅎ".split('/')  # len = 27
test = cho + jung + ''.join(jong)

hangul_length = len(cho) + len(jung) + len(jong)  # 67


def is_valid_decomposition_atom(x):
    return x in test


def decompose(x):
    in_char = x
    if x < ord('가') or x > ord('힣'):
        return chr(x)
    x = x - ord('가')
    y = x // 28
    z = x % 28
    x = y // 21
    y = y % 21
    # if there is jong, then is z > 0. So z starts from 1 index.
    zz = jong[z - 1] if z > 0 else ''
    if x >= len(cho):
        print('Unknown Exception: ', in_char, chr(in_char), x, y, z, zz)
    return cho[x] + jung[y] + zz


def decompose_as_one_hot(in_char, warning=True):
    one_hot = []
    # print(ord('ㅣ'), chr(0xac00))
    # [0,66]: hangul / [67,194]: ASCII / [195,245]: hangul danja,danmo / [246,249]: special characters
    # Total 250 dimensions.
    if ord('가') <= in_char <= ord('힣'):  # 가:44032 , 힣: 55203
        x = in_char - 44032  # in_char - ord('가')
        y = x // 28
        z = x % 28
        x = y // 21
        y = y % 21
        # if there is jong, then is z > 0. So z starts from 1 index.
        zz = jong[z - 1] if z > 0 else ''
        if x >= len(cho):
            if warning:
                print('Unknown Exception: ', in_char, chr(in_char), x, y, z, zz)

        one_hot.append(x)
        one_hot.append(len(cho) + y)
        if z > 0:
            one_hot.append(len(cho) + len(jung) + (z - 1))
        return one_hot
    else:
        if in_char < 128:
            result = hangul_length + in_char  # 67~
        elif ord('ㄱ') <= in_char <= ord('ㅣ'):
            result = hangul_length + 128 + (in_char - 12593)  # 194~ # [ㄱ:12593]~[ㅣ:12643] (len = 51)
        elif in_char == ord('♡'):
            result = hangul_length + 128 + 51  # 245~ # ♡
        elif in_char == ord('♥'):
            result = hangul_length + 128 + 51 + 1  # ♥
        elif in_char == ord('★'):
            result = hangul_length + 128 + 51 + 2  # ★
        elif in_char == ord('☆'):
            result = hangul_length + 128 + 51 + 3  # ☆
        else:
            if warning:
                print('Unhandled character:', chr(in_char), in_char)
            # unknown character
            result = hangul_length + 128 + 51 + 4  # for unknown character

        return [result]


def decompose_str(str):
    return ''.join([decompose(ord(x)) for x in str])


def decompose_str_as_one_hot(str, warning=True):
    # print(str)
    tmp_list = []
    for x in str:
        da = decompose_as_one_hot(ord(x), warning=warning)
        tmp_list.extend(da)
    return tmp_list


def data_li(file="", index=""):
    da = pd.read_excel(file)
    da_name = [decompose_str(str(i)) for i in da[index]]
    da['sub'] = da_name
    # for num, i in enumerate(da[index]):
    #     if len(i) <= 1:
    #         da = da.drop(num, axis=0)
    da = da.reset_index().iloc[:, 1:]
    return da


def result_csv(da, columns, po_li, neg_li, po_word, neg_word, f_name):
    dat = pd.DataFrame(columns=columns)
    dat = pd.concat([da, dat])

    for j in range(len(po_li)):
        word = []
        classifi = []
        for n, i in (enumerate(po_word['sub'])):
            if i in po_li[j][1]:
                if len(str(po_word.iloc[n, 2])) > 1:
                     spl = str(po_word.iloc[n, 2]).split(',')
                     for j in range(len(spl)):
                         word.append(po_word.iloc[n, 1])
                         classifi.append(spl[j])
                else:
                    word.append(po_word.iloc[n, 1])
                    classifi.append(po_word.iloc[n, 2])
        dat.iloc[po_li[j][2], 3] = pd.Series([word])# 포함된 단어
        dat.iloc[po_li[j][2], 2] = pd.Series([classifi])# 세부 분류

    for j in range(len(neg_li)):
        word = []
        classifi = []
        for n, i in (enumerate(neg_word['sub'])):
            if i in neg_li[j][1]:
                if len(str(neg_word.iloc[n, 2])) > 1:
                     spl = str(neg_word.iloc[n, 2]).split(',') #[0,2]  [0,1,2]
                     for j in range(len(spl)):
                         word.append(neg_word.iloc[n, 1])
                         classifi.append(spl[j])
                else:
                    word.append(neg_word.iloc[n, 1])
                    classifi.append(neg_word.iloc[n, 2])
        dat.iloc[neg_li[j][2], 3] = pd.Series([word])# 포함된 단어
        dat.iloc[neg_li[j][2], 2] = pd.Series([classifi])# 세부 분류
    dat.to_excel(f"results/{f_name}.xlsx", index=False)
