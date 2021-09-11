import pandas as pd
from datetime import datetime

def reset_and_duplicates(ex):
    ex.drop_duplicates(['word'], keep='first', inplace=True)
    ex.dropna(subset=['word'], inplace=True)
    ex = ex.reset_index(drop=True)
    d = datetime.now()
    ex.to_excel('감정분류파일/%02d%02d슬픔.xlsx' % (d.month, d.day), index=False)

if __name__ == '__main__':
    """
    data index reset  및 중복제거
    """
    ex = pd.read_excel("감정분류파일/슬픔data.xlsx")
    reset_and_duplicates(ex)