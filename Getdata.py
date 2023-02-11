"""
Created: Dec 2019

object: 
Python 網路爬蟲功能由「公開網站」得得到所需資訊

author: P16081203

enviroment + package:
(anacoda + spyder) + (requests + BeautifulSoup + pandas + time)
but can also work on thonny+requests+BeautifulSoup+pandas
if you don't have, just go to anacoda prompt
activate ...(if you have envirment)
conda install ...
Note that you should install on the the envirment that you want to run    
"""


import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup




#               指數
# get data one url by one
def get_IEX(url_IEX):
    # 由requests提出網路的請求並提交表單，將結果儲存到變數page中
    page = requests.get(url_IEX)
    
    # 將網頁原始碼丟給BeautifulSoup解析
    #print(page.text)
    html = soup(page.text, "html.parser")
    
    # for storage
    data = []
    data_IEX = []
    col_IEX = [" 日期: "," 開盤指數: "," 最高指數: "," 最低指數: "," 收盤指數: " ]
    # get table
    Time_table = html.find("table")
    # get tr from table
    Time_table = Time_table.find_all("tr")
    for i in range(len(Time_table)):
        # skip first 2 lines
        if i < 2:
            continue
        # tmp for data
        tmp = []
        # get td from every tr(runs)
        td = Time_table[i].find_all("td")
        for j in range(len(td)):
            if j == 0:
                a = td[j].text
                tmp.append(a)
                continue
            # get text in a in each td(td[i])
            a = td[j].text.split(',')
            a1 = a[1].split('.')
            # append tmp for data
            tmp.append(1000 * float(a[0]) + float(a1[0]) + 0.01 * float(a1[1]))
        # append data
        data_IEX.append(tmp)
        data.append(tmp[4])
    # show
    #print(len(data_IEX))
    # return
    return sum(data) / len(data)
# for storage
data_IEX = []
# 選擇要爬蟲的網址
mon = [ '01', '02' , '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]
#for i in range(1999,2019):
for i in range(1999,2000):
    for j in range(0,12):
        url_IEX = 'https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=html&date=' + str(i) + mon[j] + '01'
        data_IEX.append([ get_IEX(url_IEX) ])
        time.sleep( 44 )




#               進出口
# 選擇要爬蟲的網址
url_Port = "http://web02.mof.gov.tw/njswww/WebProxy.aspx?sys=220&ym=8801&ymt=10712&kind=21&type=1&funid=i8301&cycle=41&outmode=0&compmode=00&outkind=11&fldspc=2,4,&rdm=ej2lmneW"

# 由requests提出網路的請求並提交表單，將結果儲存到變數page中
page = requests.get(url_Port)

# 將網頁原始碼丟給BeautifulSoup解析
#print(page.text)
html = soup(page.text, "html.parser")

# for storage
data_Port = []
col_Port = [" 數量指數-出口: "," 數量指數-進口: "," 單位價值指數-出口: "," 單位價值指數-進口: " ]
# " 編號: " in th
#col_Port = [" 編號: "," 數量指數-出口: "," 數量指數-進口: "," 單位價值指數-出口: "," 單位價值指數-進口: " ]
# get table
Index_table = html.find("table", {"class":"tblcls"})
#Index_table = html.find("table", {"summary":"統計資料庫查詢結果網頁表格資料"})
# get tr from table
Index_table = Index_table.find_all("tr")
# skip 88 ~ 107
skip = []
#for i in range(88,108):
for i in range(88,89):
    skip.append(str(i) + '年')
for i in range(len(Index_table)):
    # skip first line
    if i == 0:
        continue
    # skip 107 108, ... year
    ck = 0
    for j in range(len(skip)):
        if Index_table[i].find("th").text == skip[j]:
            ck = 1
            break
    if ck == 1:
        continue
    # tmp for data
    tmp = []
    # get td from every tr(runs)
    td = Index_table[i].find_all("td")
    for j in range(len(td)):
        # get text in a in each td(td[i])
        a = td[j].find("a").text
        # append tmp for data
        tmp.append(float(a))
    # append data
    data_Port.append(tmp)
print(len(data_Port)) 




# contensate
col = [" 收盤指數: "," 數量指數-出口: "," 數量指數-進口: "," 單位價值指數-出口: "," 單位價值指數-進口: "]
data = []
for i in range(len(data_IEX)):
    data.append( data_IEX[i] + data_Port[i] )




# using pandas to output
# dataframe
df = pd.DataFrame(data, columns = col)
df.to_csv('All.csv', index = False)