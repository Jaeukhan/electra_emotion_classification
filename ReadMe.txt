"""폴더 설명"""

1] checkpoint
electra_827.pt - 8월 27일에 네이버리뷰+2100개부정 문장으로 학습한. electra model(deeplearning) 학습한 파라미터.

2] train_data
ratings_train.txt - 네이버 리뷰 train data txt파일
827.txt - 네이버리뷰 + 부정data2100개 추가 <거의 긍정:부정 7:3비율>
0827슬픔.xlsx -슬픔 data 2100개 엑셀(지금까지 마링에서 부정 문장 모아 놓은 엑셀파일)

3] utils(Folder)
#이폴더는 안건들여도 됩니다(기능을 수정할 때 빼고는)
decompostion.py - 사전에서 단어를 subword로 바꿔주는 기능을 가짐. ex) 안녕 => ㅇ ㅏ ㄴ ㄴ ㅕ ㅇ
utills.py -현재 정리중인 폴더이며, excel파일=>json파일로 바꿔주는 기능, 사전 중복제거 해주는 기능을 가지고 있음 (안드로이드에 넣을때 json으로 바꿔줘야해서 쓰임)


4] 감정분류파일
0826_부정사전전처리_V4(라벨링체크), 0828_긍정사전전처리_V2(라벨링체크) - 현재 사용하는 사전

5] 사전작업
알바 이용해서 사전 처리시 여기다 넣어 놓고 사용했음. 여기 있는 엑셀파일을 utils폴더 프로그램을 이용해서 중복 지우고 concat을하면 됩니다.

6] 밖에 나와있는 py파일들 설명.
train.py   새로운 데이터로 딥러닝 학습이 필요할시 사용하면 될거 같습니다.
test.py    감정분류가 되는지 볼떄 사용. 결과는 날짜_붙여준이름.xlsx로 나옴. 0828_긍정.xlsx
traindatagenerate.py - 기존traindata에다가 새로 들어온 문장데이터 더해준는 py파일
data_arrange.py - 전처리 기능 (짧은 단어제거, 중복제거 등)
IndexResetandDuplicate - 엑셀 불러와서 중복 제거.
	
7]results Folder
test.py로 돌린 결과를 모아놓은 폴더

현재 test시 사용하는 것은 학습데이터로 사용하지 않은 감사.xlsx(사전작업폴더)를 사용중.



""" 파이선 프로그램 돌릴 시 기능 설명"""

1) 추가적인 사전작업이 필요한경우
data_arrange.py 파일을 실행하여, pd.read_excel('파일명')에 파일명을 입력한 후 돌리면, 기존 사전과 알바를 이용해서 나온 사전이 합쳐져서 저장 된다. 
저장은 감정분류파일에 슬픔data.xlsx 엑셀 파일로 저장.

2) 딥러닝 모델에 추가적인 문장을 추가하여 학습해야하는 경우
* train data를 새로 만들어야하는 경우 적용
traindatagenerate.py를 실행하여 TrainData_Structure('파일명', '긍정' or '부정')에 파일명과 긍정인지 부정인지 입력 하면, train_data_(month)(day).txt가 적힌 txt생성
train.py 파일에 train_txt_name = "파일명" 파일명을 바꿔준 후 train시 checkpoint에 학습한 결과가 생성됨. 파일명은 electra_(month)(day).pt 

3) 트레인 된 결과를 감정분류가 잘되는지 테스트 해봐야하는 경우
test.py 실행 후 
excel_name에 테스트 할 엑셀 이름을 넣어주고, 원래 일기파일이을 넣어주는 부분
save_excel_name = "파일명" 저장하고 싶은 파일 이름을 입력해주면됨.
pt_file_name은 2번에서 train해서 나온 학습한 결과에 이름을 넣어주면됨. 아니면 그대로 사용하시면 됩니다.
저장은 results 폴더내에 저장 되며, save_excel_name에서 작성한 이름으로 엑셀파일로 저장됩니다.

