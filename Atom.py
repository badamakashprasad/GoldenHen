import requests
import os
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import time
import zipfile
import sqlite_db_maker as sql
import urllib.request
import pickle
from datetime import date,timedelta,datetime
from multiprocessing import Pool





#------------------------------------------   Singular return function   ---------------------------------------------







def is_open_time(now  = timedelta(hours = datetime.now().hour,minutes = datetime.now().minute)):
    fr =  timedelta(hours = 9,minutes = 0)
    to = timedelta(hours = 15,minutes = 30)
    if fr > now and now > to:
        return True
    else:
        return False


def get_latest_open_day(today = date.today()):
    if not today.weekday() in (5,6) and not today in HOLIDAYS:
        return today
    else:
        return get_latest_open_day(today - timedelta(days = 1))




download_data = lambda path,url,name : open(name,'wb').write(requests.get(url,allow_redirects=True).content)
push_object = lambda name,obj : pickle.dump(obj,name)
pull_object = lambda name : pickle.load(open(name,"rb"))
cln = lambda _ : _.strip()




#------------------------------------------        PATH          ----------------------------------------------------






HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}
HOLIDAYS = []
BHAVCOPY_URL = "https://www1.nseindia.com/content/historical/DERIVATIVES/2020/FEB/fo{}{}{}bhav.csv.zip".format(get_latest_open_day().day,get_latest_open_day().strftime("%b").upper(),get_latest_open_day().year)
QUOTE_URL =  lambda symbol : "https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}".format(symbol.upper())
PATH = lambda x : "Nifty_data\\{}\\{}".format(x.strftime("%d-%m-%y"),x.strftime("%H_%M_%S"))



#------------------------------------------    Base functions    ----------------------------------------------------


def get_json_link(name,path):
    with open(path,'r') as csvfp:
        dictData = csv.DictReader(csvfp)
        for row in dictData:
            if row['Name'] == name:
                return row['Json Link']


def get_json_data(link):
    try:
        print("executing {}".format(link))
        data = json.loads(requests.get(link,headers = HEADERS).content)
        timestamp = data['time']
    except ValueError:
        print("Error in retriving : {} Retrying in 5 secs...".format(link))
        time.sleep(5)
        get_json_data(link)
    return data['data'],timestamp



def get_quote_json(symbol):
    data = requests.get(QUOTE_URL(symbol),headers = HEADERS).content
    soup = BeautifulSoup(data,"html.parser")
    ls = soup.find("div",{"id" : "responseDiv"})
    ret = json.loads(ls.get_text().strip())
    return ret




def get_info_companies(symbol):
        info_dict = {}
        info_url = f'https://www1.nseindia.com/marketinfo/companyTracker/compInfo.jsp?symbol={symbol}&series=EQ'
        data = requests.get(info_url,headers = HEADERS).content
        soup = BeautifulSoup(data,features="lxml")
        for a in soup.find_all('td'):
            if a.find('b') is None:
                break
            elif a.find('b').get_text().find(":") is not -1:
                temp_info_ls = a.get_text().split(":")
                info_dict[cln(temp_info_ls[0])] = cln(temp_info_ls[1])
        return info_dict


#----------------------------------------    Runnable functions    --------------------------------------------------

def get_all_Nifty_csv(t):
    path = PATH(t)
    os.makedirs(path,exist_ok=True)
    with open('nseJsonListing.csv','r') as fp:
        dictdata = csv.DictReader(fp)
        for row in dictdata:
            link = row['Json Link']
            try:
                data = get_json_data(link)
            except ValueError:
                print("Error in retriving json data | filename : {}".format(row['Name']))
            columns = [i for i in data[0]]
            with open(path+'\\'+row['Name']+'.csv','w',newline='') as fpw:
                writer = csv.DictWriter(fpw,fieldnames = columns)
                writer.writeheader()
                writer.writerows(data)
                #print("{} done".format(row['Name']))
        print("All data retrived --> {}".format(datetime.now()))


# def make_csv(path):
#     with open(path,newline='') as fp:






def get_watch_list_csv():
    pass
