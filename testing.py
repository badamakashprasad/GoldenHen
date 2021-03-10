import time
import random
import pandas as pd
import json
import requests 
import csv
import os
from datetime import datetime
from collections import OrderedDict
import Atom as base
import logging


HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}

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



def isSimilar_ret(csv_data,ret_data):
    *_,last = csv_data
    if last['ltP'] == ret_data['ltP']:
        if ret_data['timestamp'] not in [tp['timestamp'] for tp in csv_data]:
            return True
    return False


fg_t = None
url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'
#print(requests.get(url).content)
path = 'D:\\GoldenHen\\NSE_testing'
df_ls = pd.read_csv('D:\\GoldenHen\\NSE_data\\all_companies_list.csv')
print("Requesting from {}".format(url))
data,timestamp = get_json_data(url)
print("\nRequest acheived of {}\n".format(url))
print("Updating data of {}".format(url[url.rfind('/')+1:]))
for i in range(len(data)):
    ls = []
    d = data[i]
    
    #print(df_ls[df_ls['Symbol'] == d['symbol']])
    try:
        ls = df_ls[df_ls['Symbol'] == d['symbol']].values.tolist()[0]
        fg_t = False
    except IndexError as e:
        info_dict = base.get_info_companies(d['symbol'])
        ls.extend([0,'','',''])
        for key in info_dict:
            ls.append(info_dict[key])
        print(d['symbol'],e)
        #print(d['symbol'],e)
        fg_t = True
    #ls = df_ls[df_ls['Symbol'] == d['symbol']].values.tolist()[0]
    #print(ls)
    if fg_t is True:
        print(ls)
    d['Company Name'] = ls[2]
    d['Market Capitalization'] = ls[3]
    d['Date of Listing'] = ls[4]
    d['Face Value'] = ls[5]
    d['ISIN Code'] = ls[6]
    d['Industry'] = ls[7]
    d['timestamp'] = timestamp   
    columns = [*d]
    #print(columns,type(columns))
    filename = path+'\\'+d['symbol']+'.csv'
    #print(d['symbol'])
    if os.path.isfile(filename):
        with open(filename,'r',newline='') as fp:
            reader = csv.DictReader(fp,fieldnames = columns)
            similar = isSimilar_ret(reader,d)
            fp.close()
        if similar:
            with open(filename,'+a',newline='') as fp:
                writer = csv.DictWriter(fp,fieldnames = columns)
                writer.writerow(d)
                fp.close()

    else:
        with open(filename,'w',newline='') as fp:
            writer = csv.DictWriter(fp,fieldnames = columns)
            writer.writeheader()
            writer.writerow(d)
            fp.close()
print('Data stored of {}'.format(url[url.rfind('/')+1:]))
print('-'*50)



# import logging
# logging.basicConfig(filename='NSE_data_log.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


# from tqdm import tqdm

# for i in tqdm(range(100)):
#     print(i)
