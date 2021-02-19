import requests
import os
import copy
from bs4 import BeautifulSoup
import csv
import re
import datetime
import urllib.request
import shutil
import pandas as pd
import variable_data as vd
from tqdm import tqdm




cln = lambda _ : _.strip()
def get_info_companies(symbol):
        info_dict = {}
        info_url = f'https://www1.nseindia.com/marketinfo/companyTracker/compInfo.jsp?symbol={symbol}&series=EQ'
        data = requests.get(info_url,headers = vd.HEADERS).content
        soup = BeautifulSoup(data,features="lxml")
        for a in soup.find_all('td'):
            if a.find('b') is None:
                break
            elif a.find('b').get_text().find(":") is not -1:
                temp_info_ls = a.get_text().split(":")
                info_dict[cln(temp_info_ls[0])] = cln(temp_info_ls[1])
        return info_dict

def get_latest_nse_all_companies_list(path,name):
    print("Extraction of all companies of NSE Started")
    data = requests.get(vd.ALL_COMPANY_LIST_URL,headers = vd.HEADERS).content
    soup = BeautifulSoup(data,features="lxml")
    blk = soup.find('div',{'class':'midContainer'})
    l = []
    for i in blk.findAll('a'):
        match = re.search(r'\w+ \d{2}, \d{4}',i.get_text())
        date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
        l.append([date,i.get('href')])
    url = [i for i in l if i[0] == max([i[0] for i in l])][0][1]
    url = 'https://www1.nseindia.com/corporates/compliance/' + url[url.rfind('/')+1:]
    tmp_fileName = os.path.join(path, name+'.xlsx')
    with urllib.request.urlopen(url) as response, open(tmp_fileName, 'wb') as out_file:
        out_file.write(response.read())
    
    print(f"Temporary file retrieved : {tmp_fileName}")

    df = pd.read_excel(tmp_fileName,index_col=0)
    

    for symbol in tqdm(df['Symbol'],desc="Extracting"):
        info_dict = get_info_companies(symbol)

        for key in info_dict:  
            df.loc[df['Symbol'] == symbol,key] = info_dict[key]
    
    df.drop('Unnamed: 4',axis=1,inplace=True)
    df.to_csv(os.path.join(path,name+".csv"))

    print(f"File saved\nLocation path : {path}      filename : {name}.csv")

    print("deleting temporary file")
    if os.path.exists(tmp_fileName):
        os.remove(tmp_fileName)

    print("Extraction of all companies of NSE Completed")
    pass



def remove_duplicate(path):
    print(f'Removing duplicate rows from all the files of path : {path}')
    for fileName in tqdm(os.listdir(path),desc='Duplicate Removing'):
        uni_data = []
        with open(fileName,'r',newline='') as fp:
            reader = csv.DictReader(fp)
            first,*data = reader
            uni_data = [first]
            for i in range(1,len(data) - 1):
                #rRprint(data[i]['timestamp'],[_['timestamp'] for _ in uni_data])
                if data[i]['timestamp'] not in [od['timestamp'] for od in uni_data]:
                    uni_data.append(data[i])
            fp.close()
        #uni_data = [list(_.values()) for _ in uni_data]
        with open(fileName,'w',newline='') as fp:
            writer = csv.DictWriter(fp,fieldnames=uni_data[0].keys())
            writer.writeheader()
            writer.writerows(uni_data)
            fp.close()
    print("Removing duplicated rows completed")
    pass



########################## FUNCTION EXECUTION AREA ##########################


#get_latest_nse_all_companies_list(path = vd.NSE_PATH, name = vd.NSE_ALL_COMPANY_LIST_FILENAME)
#remove_duplicate(vd.NSE_COMPANY_DATA_PATH)


