# -*- coding: utf-8 -*-
import datetime
import MySQLdb #ubuntu
conn= MySQLdb.connect("localhost", "root","chlee","finance")
curs=conn.cursor()
import csv
f=open('./list.csv','r') # 종목 리스트 csv 로드
dataread=f.readlines()
data=[]
for i in dataread:
	data.append(i[:-1]) # 뒤에 공백 불러오는 것 삭제

cols=['total_assets','total_liabilities', 'sales_figures','sales_cost','business_profits','gross_margin','current_income','depreciation_expense_of_tangible_assets','liquid_asset','noncurrent_asset','liquid_liability']
#now=datetime.datetime.now()
#date_time = datetime.datetime.now() #  현재 날짜 까지 받음
date_time = datetime.datetime.strptime('2017-03-13 12:23:38', '%Y-%m-%d %H:%M:%S') # 현재 디비에 업데이트된 마지막 날짜를 입력.
mysql_time = date_time.strftime('%Y-%m-%d') # 초 분을 없애고 날짜만 얻기 위해서
final_date= '2004-01-01' # 최 하단에 있는 날짜. 즉 2004-01-01 부터 카피

def DateCounter():
    global mysql_time
    global date_time
    yesterday = date_time- datetime.timedelta(days=1) # 하루를 빼서 그 전날을 구함
    date_time = yesterday
    mysql_time = date_time.strftime('%Y-%m-%d') # 왜 이렇게 여러번 걸쳐서 하냐면 초, 분을 없애야되기 때문임

def Get_value(colname,table,time):
    sql= "select "+ colname + " from " + table + " where date = '"+ time +"'"# 특정 날짜의 컬럼 값을 구한다 (복사할 값)
    curs.execute(sql)
    result = curs.fetchall() # 특정날짜의 값
    for row in result:
        global x
        x= row[0] # 전역변수 x에 입력

def CopyUpdate(start, end,colname,table,val): # 카피한 값을 디비에 업데이트 하는 부분
    updatesql= "update finance."+table+ " set "+ colname + " = "+ val + " where (date >'"+ start +"')" + " and (date<='"+ end +"')" #해당 값을 그 날짜부터, 최신쪽의 데이터가 없었던 날짜까지 다 카피 합니다.
    print updatesql # 출력
    curs.execute(updatesql) #쿼리
    conn.commit() # 커밋

def StartFinding(colname,table,end_date):
    while (mysql_time>=final_date): # 한날짜씩 전으로 카운트 다운 하는데 final_date(2004-01-01)이 되면 반복문이 멈춤
        DateCounter() # 날짜를 하루전씩으로 이동
        Get_value(colname,table,mysql_time) # 계속 전의 날짜의 데이터 값을 구합니다.
        if x is not None: # 만일 데이터를 발견한다면, 그 날짜부터 데이터가 없었던 곳까지 데이터를 카피합니다.
            print "start filling"
            temp_start= mysql_time #데이터를 발견한 날짜부터
            temp_copy_col=str(x) #얻은 값 (있는 데이터)
            CopyUpdate(temp_start,end_date,colname,table,temp_copy_col) # 그 날짜부터 데이터가 없던 날짜까지 카피
            break

def Date_initialize(): # 한 종목의 한 컬럼의 탐색이 끝나면 다시 최신날짜로 돌려주어야하기때문에 돌립니다.
    global date_time
    date_time = datetime.datetime.strptime('2017-02-28 12:23:38', '%Y-%m-%d %H:%M:%S')
    global mysql_time
    mysql_time = date_time.strftime('%Y-%m-%d') #시간, 분 초를 짜른 날짜만을 대입

def Program(colname,table):
    Date_initialize() # 한 반복문이 끝나면 다시 날짜 최신으로 돌림
    while (mysql_time >=final_date):# 한날짜씩 전으로 카운트 다운 하는데 final_date(2004-01-01)이 되면 반복문이 멈춤
        DateCounter() # 한날짜씩 전으로 이동
        Get_value(colname,table,mysql_time) # 그 날짜의 값을 구한다.
        if x is None: # 만일 값이 없는것을 발견한다면
            print table # 프린트문
            print "None found, Start Finding "# 프린트문 : "   " 종목에서 값이 없는것을 찾았기 때문에 값이 있을때 까지 아래로 탐색하겠습니다.
            temp_end = mysql_time # 값 없는 날짜 기억
            StartFinding(colname,table,temp_end)# 처음 값이 없었던 곳을 기억해야 합니다, 함수 내에서 찾으면 그날짜까지 업데이트해야되기 때문


# 실행하면 됩니다.
print "start"


for i in range(0,len(data)):
    for k in range (0, len (cols)):
        Program(cols[k],data[i])
