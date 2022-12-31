# 한투
import mojito

# pretty print
import pprint

# 시간
import datetime
from pytz import timezone

# 크롤링
import requests
from bs4 import BeautifulSoup

# 주식데이터
import yfinance as yf
import FinanceDataReader as fdr
import pandas as pd





### 변수 선언란

# 크롤링
url = 'https://finance.yahoo.com/quote/%5ENDX/'
response = requests.get(url)

# 기초 계좌정보 연결
mock_acc = open("mock.key", 'r')   # real_acc = open("real.key", 'r')            # 실제 계좌
lines = mock_acc.readlines()
key    = lines[0].strip()
secret = lines[1].strip()
acc_no = lines[2].strip()                                                        # 모의 계좌

# 상위 10개 기업 리스트
top10_stock_list = []





### 함수 작성란

# NASDAQ-100 크롤링
def get_ndx():

    if response.status_code == 200:
    
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # HTML 태그 내 클래스명으로 검색, 텍스트 추출
        ndx_class = soup.find(class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
        ndx = ndx_class.get_text()

    else :
        print(response.status_code)
    
    return ndx


# 기초정보고시
def my_acc():

    print("나스닥 100 지수는 " + get_ndx() + "이며, ")

    # 미국 현지 시간
    cur_time_US_raw = datetime.datetime.now(timezone('America/New_York'))
    cur_time_US = cur_time_US_raw.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    print("미국 뉴욕 현지 시간은 " + str(cur_time_US) + " 입니다.")

    bullet = broker.fetch_present_balance()                                      # 잔고조회
    print("총자산평가 : " + bullet['output3']['tot_asst_amt'])
    # print("출금가능 외화 : " + str(bullet['output2']['frcr_drwg_psbl_amt_1']))
    # print("출금가능 원화 : " + bullet['output2']['frcr_evlu_amt2'])


def top10_stock_list_maker():

    # FinanceDataReader, 거래소 + 시총 상위 10위 기업
    df_nsq = fdr.StockListing('NASDAQ')

    for i in range(10):
        top10_stock_list.append(df_nsq.iloc[i, 0]) # 행, 열


# 매수종목선정함수
def stock_selector():

    # 달러잔고 or ETF 소유 시 전량매도 및 환전
    # print("총외화잔고합계는 " + bullet['output3']['tot_frcr_cblc_smtl'] + "원 입니다.")

    fstock = yf.Ticker(top10_stock_list[0]).info["marketCap"]                   # 시가총액 1위
    sstock = yf.Ticker(top10_stock_list[1]).info["marketCap"]                   # 시가총액 2위

    print("나스닥 시가총액 1위 기업은 " + top10_stock_list[0]
        + "나스닥 시가총액 2위 기업은 " + top10_stock_list[1])

    if (sstock - fstock) * 100 / sstock > 10:                                   # 1,2위 기업간 시총이 10% 이상 차이날 때
        divider = False
    else:
        divider = True
    
    return divider


def stock_buying(divider):

    info_fstock = broker.fetch_price(top10_stock_list[0])                       # 시총 1위 기업정보
    info_sstock = broker.fetch_price(top10_stock_list[1])                       # 시총 2위 기업정보

    if divider == True:                                                         # 두 기업의 시가총액이 10% 이상 차이난다면
        print("시총 1, 2위 기업 간 차이 심함")
        resp     = broker.create_limit_buy_order(                               # 1위 기업만 매수
            symbol   = top10_stock_list[0],
            price    = info_fstock['output']['last'],
            quantity = 1
        )
        print(resp)

    elif divider == False:                                                      # 그렇지 않은 경우
        print("시총 1, 2위 기업 간 차이 심하지 않음")
        resp     = broker.create_limit_buy_order(                               # 1위, 2위 기업 매수
            symbol   = top10_stock_list[0],
            price    = info_sstock['output']['last'],
            quantity = 1
        )
        pprint.pprint(resp)

        resp     = broker.create_limit_buy_order(
            symbol   = top10_stock_list[1],
            price    = 30,
            quantity = 1
        )
        pprint.pprint(resp)


def crisis_activated():
    print("임시 코드")





### 실질 코드란

if __name__=="__main__":

    while True:
        # 증권사 객체 생성
        broker = mojito.KoreaInvestment(
        api_key = key,
        api_secret = secret,
        acc_no = acc_no,
        exchange = '나스닥',
        mock = True                                                             # 모의투자 여부
        )
        
        # 자산고지
        my_acc()

        # 상위 10개 기업 산출
        top10_stock_list_maker()

        # 매수종목선정함수 및 매수
        stock_buying(stock_selector())

        bullet = broker.fetch_present_balance()
        pprint.pprint(bullet)

        # 딜레이 조건 이곳에 입력
        # code





''' 메모

# base	전일종가
# pvol	전일 거래량
# last	당일 조회시점의 현재가격
# tvol	당일 조회시점까지의 전체 거래량
# tamt	당일 조회시점까지의 전체 거래금액



# 주문 코드
resp = broker.create_limit_sell_order(
symbol="APPL",
price=30,
quantity=1
)

pprint.pprint(resp)



# pykis

pykis
https://github.com/pjueon/pykis



# 데이터프레임 접근
dataframe.iloc[i, 0]와 같이 행, 열 순이다.

'''