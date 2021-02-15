import Atom as base
import multiprocessing
import time
import random
import pandas as pd
import json
import requests 
import csv
import os
import logging
from datetime import datetime
from collections import OrderedDict

logging.basicConfig(filename='NSE_data_log.log', level=logging.DEBUG)
HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}

# def get_json_data(link):
#     try:
#         #print("executing {}".format(link))
#         data = json.loads(requests.get(link,headers = HEADERS).content)
#         timestamp = data['time']
#     except ValueError:
#         print("Error in retriving : {} Retrying in 5 secs...".format(link))
#         time.sleep(5)
#         get_json_data(link)
#     return data['data'],timestamp




def statement_(reader,d):
    data = OrderedDict(d)
    *_,last = reader
    del data['timestamp']
    del last['timestamp']
    if set(last.items()).intersection(set(data.items())) is not None:
        return False
    else:
        return True

 

def worker(input_queue):
    while True:
        url = input_queue.get()

        if url is None:
            break
        #url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'
        path = 'NSE_data'
        #df_ls = pd.read_csv('ind_nifty500list.csv')
        df_ls = pd.read_csv('NSE_data/all_companies_list.csv')
        print("Requesting from {}".format(url))
        data,timestamp = base.get_json_data(url)
        print("\nRequest acheived of {}\n".format(url))
        print("Updating data of {}".format(url[url.rfind('/')+1:]))
        for i in range(len(data)):
            d = data[i]
            try:
                ls = df_ls[df_ls['Symbol'] == d['symbol']].values.tolist()[0]
            except IndexError as e:
                info_dict = base.get_info_companies(d['symbol'])
                ls.extend([0,'','',''])
                for key in info_dict:
                    ls.append(info_dict[key])
                logging.error(d['symbol']+' : '+str(e))
            
            d['Company Name'] = ls[2]
            d['Market Capitalization'] = ls[3]
            d['Date of Listing'] = ls[4]
            d['Face Value'] = ls[5]
            d['ISIN Code'] = ls[6]
            d['Industry'] = ls[7]
            d['timestamp'] = timestamp           
            columns = [i for i in d] 
            filename = path+'\\'+d['symbol']+'.csv'
            if os.path.isfile(filename):
                with open(filename,'r',newline='') as fp:
                    reader = csv.DictReader(fp,fieldnames = columns)
                    flag =  statement_(reader,d)
                    fp.close()
                if flag:
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


def master():
    df = pd.read_csv('nseJsonListing.csv')
    urls = df['Json Link'].values
    input_queue = multiprocessing.Queue()
    workers = []

    # Create workers.
    for _ in range(5):
        p = multiprocessing.Process(target=worker, args=(input_queue, ))
        workers.append(p)
        p.start()

    # Distribute work.
    for url in urls:
        input_queue.put(url)

    # Ask the workers to quit.
    for w in workers:
        input_queue.put(None)

    # Wait for workers to quit.
    for w in workers:
        w.join()


if __name__ == '__main__':
    while True:
        start = time.time()
        master()
        print("NSE data retirved in {} secs".format(time.time() - start))
        print("---------------- Timestamp : {}----------------------".format(datetime.now()))
        os.system("ping -n 3 localhost >nul")
        os.system("echo.")
        os.system("cls")