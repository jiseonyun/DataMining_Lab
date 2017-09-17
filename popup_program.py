# -*- coding: utf-8 -*-
import MySQLdb
conn=MySQLdb.connect("localhost","root","chlee","finance")  # 로컬 호스트에 디비 접속
curs=conn.cursor()
#import Tkinter
from Tkinter import * # 팝업 메세지를 열기위한
import random # 종목 랜덤으로 뽑기 위해서
import datetime # 날짜 계산하기위해서
now= datetime.datetime.now()
week= now-datetime.timedelta(days=7) # 일주일 전 날짜 계산
week= week.strftime('%Y-%m-%d') # 뒤 시간 분 초 없애기 위해서
#print week # 날짜 테스트 출력
import csv
f=open('./list.csv','r') # 종목 리스트 csv 로드
dataread=f.readlines()
data=[]
for i in dataread:
	data.append(i[:-1]) # 뒤에 공백 불러오는 것 삭제
e=open('./ecos.csv','r') # 에코스 컬럼 리스트 csv 로드
dataread=e.readlines()
ecos=[]
for i in dataread:
	ecos.append(i[:-1]) # 뒤에 공백 불러오는 것 삭제

q=open('./quandl.csv','r') # 퀀들 컬럼 리스트 csv 로드
dataread=q.readlines()
quandl=[]
for i in dataread:
	quandl.append(i[:-1]) # 뒤에 공백 불러오는 것 삭제

# ------------외부 csv 읽어서 배열에 저장 ------------

BadResult=""# global bad result query
searchResult="" # global result query
BestStock=""
def check(table,date): # 일반 항목 체크
	global searchResult
	global BadResult
	global BestStock
	table_exist="show tables like '"+table+"'" #종목이 존재하는지 여부 확인하는 쿼리문
	curs.execute(table_exist) # 쿼리 실행
	result= curs.fetchall() # 쿼리문 결과
	if len(result)>0:#종목이 존재하는지 여부 확인 - 안하면 에러날 수 있음
		sql="select date from "+ table +"  where (no_stock is null or volume is null or inst_net_trans is null  or  price is null or forn_net_trans is null or forn_num_stock is null) and (date >='"+date+"')"
		#문자열 생성 -  최근 1주일 사이에 / 종목 컬럼들 중에서 널이 있는지 : 널이 있으면 출력이 되기 때문에 0 이상 나오면 null문제가 있는 것임
		curs.execute(sql) # 쿼리 디비에 실행
		result= curs.fetchall() # result는 디비에 실행한 결과 값을 받음
		if len(result)>0: # 널이 존재한다면 : 결과의 길이가 0 이상이면 null이 있는것임 . 실제로 출력 한칸 일떄는 len이 결과값이 1 이 나옴
			BadResult+=table #팝업에 들어갈 문자열 searchResult에 해당 종목이름 추가
			BadResult+=" 이 일반 항목에서 이상이 있음\n"#팝업에 들어갈 문자열 searchResult에 이상있음을 알려줌
			sql=" select date from "+ table+" where price is null and date>='"+date+"'" # 이상이 있을 떄 가장 중요한 price를 불러오는지 체크
			curs.execute(sql) # 디비에 쿼리 실행
			result=curs.fetchall() # 결과값 출력
			if len(result) >0: # 만일 price에서 널이 출력 된다면
				if table== "a005930" or table=="a066570": # 삼성 또는 엘지면 첫 칸에 출력
					print " test"
					BestStock+=table+"samsung/lg price 문제가 있음\n" # samsung/lg
				else:
					BadResult+=table+" price를 불러오는데 문제가 있음\n" # price에 문제가 있다고 말해줌
			else: # price에 널이 없으면
				if table== "a005930" or table=="a066570":
					BestStock+=table+" samsung/lg price 문제가 없음\n" # samsung/lg
				else:
					searchResult+=table+" price 문제 없음\n" # 이 경우는 종목에서 price외의 문제임을 알려줌
		else: # -------- 종목에 널이 없고 문제 없다면면
			if table== "a005930" or table=="a066570":
				BestStock+=table+" samsung/lg Ok\n" # samsung/lg
			else:
				searchResult+=table # 종목이름 + OK 출력
				searchResult +=" OK\n"
	else:
		BadResult+= table +"table 존재x\n "
def Zcheck(table,date): # 재무제표 체크
	global searchResult #
	global BadResult
	table_exist="show tables like '"+table+"'" #종목이 존재하는지 여부 확인하는 쿼리문
	curs.execute(table_exist) # 쿼리 실행
	result= curs.fetchall() # 쿼리문 결과
	if len(result)>0:#종목이 존재하는지 여부 확인
		sql="select date from "+ table +"  where (total_assets is null or  total_liabilities is null  or  sales_figures is null or  sales_cost is null  or  gross_margin is null  or business_profits is null or  current_income is null or  depreciation_expense_of_tangible_assets is null or liquid_asset is null  or  noncurrent_asset is null  or  liquid_liability is null ) and (date >='"+date+"')"
		#최근 1주일의 재무제표 확인
		#print sql
		curs.execute(sql)
		result= curs.fetchall()
		if len(result)>0:
			BadResult+= table+ " 이 재무제표에 이상이 있음\n"
		else:
			searchResult +=table+ "재무제표 OK\n\n"

# 대표적인 삼성전자와 , lg전자의 종목명을 넣어서 개별적으로 데이터베이스에서 널을 체크한다.
check("a005930",week)
check("a066570",week)
# 주요 지표

#---- main
i=0
while(i<5):# 랜덤으로 5개 뽑아서 종목 체크
	k=random.randint(0,len(data))
	r=data[k].strip()
	check(r,week)# 랜덤으로 5개 뽑아서 종목 일반체크
	Zcheck(r,week)# 랜덤으로 5개 뽑아서 종목 재무재표 체크
	i=i+1



# daily loan check
def dailyCheck(date): # daily loan index 일반 항목 체크
	global searchResult #팝업 메세지 넣을 변수
	global BadResult
	sql="select date from finance.daily_loan_index where (kospi_idx is null or kosdaq_idx is null) and (date >='"+date+"')" # 종목이 1개기 때문에, 반복문 할 필요 없음
	curs.execute(sql) # 쿼리 실행
	result= curs.fetchall() # result에 쿼리 결과값을 출력. 정상이면 null값을 가진 항목 길이가 0이 나와야됨.
	if len(result)>0: # 만일 null이 나온다면
		BadResult+=" daily loan index 이상이 있음\n" # 이상이 있다고 출력
	else:
		searchResult +=" daily loan index OK\n" # 문제없으면 ok 출력
	# 팝업메세지 출력값에 추가

# dailyNew또한 마찬가지로 테이블이 1개이기 떄문에, 반복문을 돌리지 않음.
def dailyNewCheck(date): # 일반 항목 체크
	global searchResult
	global BadResult
	sql="select date from finance.daily_new where (cust_bal is null or cust_credit is null or fund_stock is null or fund_hyb is null or fund_bond is null) and (date >='"+date+"')"
	curs.execute(sql)
	result= curs.fetchall()# result에 쿼리 결과값을 출력. 정상이면 null값을 가진 항목 길이가 0이 나와야됨.
	if len(result)>0: # 만일 null이 나온다면
		BadResult+=" daily new 이상이 있음\n"# 이상이 있다고 출력
	else:
		searchResult +=" daily new OK\n"# 문제없으면 ok 출력

# ---- 위 정의한 함수들을 날짜값을 넣고 돌린다. -> 입력한 날짜값 이후의 데이터들을 체크한다.
dailyCheck(week)
dailyNewCheck(week)

# ---- 에코스 체크
for i in range(0,len(ecos)): # ecos[]는 컬럼이 채워진 배열임. 모든 배열 요소(컬럼들)를 반복문	
	esql="SHOW COLUMNS FROM finance.ecos like '"+ ecos[i].strip() +"'" 
	#print esql
	curs.execute(esql)
	print esql
	result= curs.fetchall()
	print result
	if len(result)>0: # 컬럼 존재할 때만 실행
		colsql="select date from finance.ecos where ("+ecos[i].strip()+" is null) and (date >='"+week+"')" # 그컬럼 널 존재하는지 확인을 한 후 ,		
		curs.execute(colsql) #쿼리를 실행해봄
		resultc= curs.fetchall()
		if len(resultc)>0:# 이상이 있다면 출력
			BadResult+="ecos:"+ecos[i].strip() +" 이상이 있음 \n"
		#else:
			#searchResult+="ecos" +ecos[i].strip() +"OK\n" # too much... 
	else:
		BadResult+="ecos:"+ecos[i].strip()+" doesn't exist\n"
		

# ---- 퀀들 체크

for i in range(0,len(quandl)):#퀀들도 모든 컬럼 다 돌아서 쿼리 실행
	sql="SHOW COLUMNS FROM finance.quandl LIKE '"+ quandl[i] +"';" # 퀀들 컬럼이 존재하는지 여부를 따지는 쿼리문
	curs.execute(sql)
	result= curs.fetchall()
	if len(result)>0: # 컬럼 존재할 때만 실행
		colsql="select date from finance.quandl where ("+quandl[i]+" is null) and (date >='"+week+"')" # 그컬럼 널 존재하는지 확인을 한 후 ,
		curs.execute(colsql)
		resultc= curs.fetchall()# 결과값을 받아와서 0 이상이면 null이 존재함.
		if len(resultc)>0:# 이상이 있다면 출력
			BadResult+="quandl"+quandl[i] +" 이상이 있음 \n"
		else:
			searchResult+=" quandl Ok"

#pop up을 위해서

root =Tk() # 최상위 창의 이름은 'root'

w=Label(root) #root와 w의 논리적은 부모자식관계 정의

w.pack() #w를 packing하여 시각적으로 보여지도록 함 -> 팝업창으로 gui바꿈
#root = Tk()

button0=Button(w)
button0['text']="<today's update>\n"+week
button0.pack() #packing
button=Button(w)
button['text']=BestStock
button.pack() #packing
button1=Button(w)
button1['text']=searchResult
button1['background']='green'
button1.pack() #packing
button2=Button(w)
button2['text']=BadResult
button2['background']='red'
button2.pack() #packing

root.mainloop()
