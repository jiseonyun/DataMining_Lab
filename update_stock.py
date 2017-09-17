# -*- coding: utf-8 -*-
# 한글 주석 가능하게 하는 것
#import pymysql
import csv
import MySQLdb
#import chardet # urf-8  인지/ euc-kr인지 타입 확인하고, 작업 진행해야함. 확인할때 필요한 임포트.
#conn= pymysql.connect("localhost", "root","9999","finance")
conn= MySQLdb.connect("localhost", "root","chlee","finance") # 교수님 디비에 접속
curs=conn.cursor()

import csv
with open('./names.csv') as f:# 데이터 가이드 항목을 저장한 파일
    reader = csv.reader(f,delimiter = ",")
    global colrows
    colrows = len(list(reader))

print "항목 길이"# 세로 길이를 구함
print colrows

data=open('./names.csv')# 데이터 가이드 항목을 저장한 파일
reader= csv.reader(data)
colList=[]
for line in reader:
    colList.append(line)
# 한글 / 디비 이름 2줄이기때문에 세로줄만 구하면 colrows,가로 2줄이기 때문에 가로는 안구함


def Check(colname):
    for k in range(0,colrows): #앞에서 구한 길이까지를 포문의 범위로 !
        if colname== colList[k][0].decode('euc-kr').encode('utf-8'):# 만일 행k 번째와 일치하면
            return colList[k][1] # 열 k로 대치

with open('./example.csv') as f: # 데이터가이드에서 불러온 파일
    reader = csv.reader(f,delimiter = ",")
    global rows
    rows = len(list(reader)) # 데이터가이드 파일의 세로 끝을 구하는 작업

print"전체 세로 길이"
print rows


data=open('./example.csv')
reader= csv.reader(data)
list=[]
for line in reader:
    list.append(line)
cols= len(line) # 가로로 몇줄 있는지 구하는 작업

#print list[8][1]#stock name
#col = list[12][1].decode('euc-kr').encode('utf-8')#chardet으로 Euc-kr인것을 확인해서 decode. 하고 , encode utf로 해야지 한글이 보임 .

for i in range(1,cols): # 0번째 . 즉 첫줄은 날짜이므로 1 부터 시작
    stock= list [8][i] #8번째에 종목 이름이 있음 항상
    colname= list [12][i].decode('euc-kr').encode('utf-8') # 한글이기 떄문에 디코드 , 인코드 해주어야함
    #print stock+ colname
    colname=Check(colname)
    #print stock+ colname
    table_exist="show tables like '"+stock+"'" #종목이 존재하는지 여부 확인하는 쿼리문
    curs.execute(table_exist)# 쿼리 실행
    result= curs.fetchall() # 쿼리문 결과
    if len(result)>0:#종목이 존재하는지 여부 확인
        for k in range(14,rows): # 14번째부터 데이터 값이 들어있음
            date= list[k][0] # 해당 행과 같은 데이터
            col=list[k][i] # 위와 같음
            col=col[:-1]# 숫자뒤에 공백 한칸씩 없애기 위해서
            if len(col)>0: #업데이트할 값이 있다면 / 널이 아니라면
                sql="update finance."+stock +" SET "+colname+" ='"+col +"' WHERE date='"+ date+"'" # 종목  stock에 해당날짜에, colname에 col을 입력한다.
                print sql
                curs.execute(sql) # 쿼리 실행
                conn.commit()# 커밋

conn.close()
