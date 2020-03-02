import json
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import pickle

HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}


def get_json_data(link):
    data = json.loads(requests.get(link,headers = HEADERS).content)
    print(data['data'])
    return data['data']

def get_all_nse_listed_companies():
    urls = ["https://www1.nseindia.com/education/content/reports/eq_research_reports_listed.htm",
    "https://www1.nseindia.com/education/content/reports/eq_rrl_m2z.htm"
    ]
    data = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url,headers = HEADERS).content,"html.parser")
        div = soup.find("table",{"class":"tabular_data","width":"710"})
        for tr in div.find_all("tr"):
            sub_data = []
            for td in tr.find_all("td"):
                sub_data.append(td.text)
            data.append(sub_data[:3])
    data.remove([])
    return data    
#data = get_all_nse_listed_companies()
#bin_data = pickle.dumps(data)
with open("ALL_NSE_LIST","rb") as fp:
    #pickle.dump(data,fp)
    _data = pickle.load(fp)
    pickle_data = [x for x in _data if x]
    store_data_temp = {}
    data = []
    for tup in pickle_data:
        store_data_temp['Sr'] = tup[0]
        store_data_temp['Symbol'] = tup[1]
        store_data_temp['Company'] = tup[2]
        #print(store_data_temp)
        data.append(store_data_temp)
        store_data_temp = {}
    content = json.dumps({'data' : data})
    with open('all_nse_company.json','w') as fw:
        fw.write(content)
