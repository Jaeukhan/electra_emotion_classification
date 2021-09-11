import pandas as pd
import json
from datetime import datetime


def excel2json(excel):
    for index, row in excel.iterrows():
        li.append(str(row['word']))
    for i in range(len(li)):
        li1['슬픔'] = li
    print(li1)
    with open('sad.json', 'w', encoding='UTF-8') as f:
        json.dump(li1, f, ensure_ascii=False)

def reset_and_duplicates(ex, keyword='word'):
    ex.drop_duplicates([keyword], keep='first', inplace=True)
    ex.dropna(subset=[keyword], inplace=True)
    ex = ex.reset_index(drop=True)
    d = datetime.now()
    ex.to_excel('감정분류파일/%02d%02d슬픔.xlsx' % (d.month, d.day), index=False)


if __name__ == '__main__':
    excel = pd.read_excel("감정분류파일/슬픔data.xlsx")
    excel2json(excel)