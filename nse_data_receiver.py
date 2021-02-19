import Atom as base
import variable_data as vd
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

logging.basicConfig(filename=vd.NSE_LOG_FILE,format='%(asctime)s %(levelname)-8s %(message)s' ,level=logging.DEBUG ,datefmt='%d-%Y-%m %H:%M:%S')



def isSimilar_ret(csv_data,ret_data):
    *_,last = csv_data
    if last['ltP'] == ret_data['ltP']:
        if ret_data['timestamp'] not in [tp['timestamp'] for tp in csv_data]:
            return True
    return False






def worker(input_queue):
    while True:
        url = input_queue.get()

        if url is None:
            break
        path = vd.NSE_COMPANY_DATA_PATH
        df_ls = pd.read_csv(vd.NSE_ALL_COMPANY_LIST_URI)
        print("Requesting from {}".format(url))
        data,timestamp = base.get_json_data(url)
        print("\nRequest acheived of {}\n".format(url))
        print("Updating data of {}".format(url[url.rfind('/')+1:]))
        for i in range(len(data)):
            d = data[i]
            ls = []
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
                    similar = isSimilar_ret(reader,d)
                    fp.close()
                if not similar:
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
    df = pd.read_csv(vd.NSE_INDICES_PATH)
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
        logging.info("NSE data retirved in {} secs".format(time.time() - start))
        print("---------------- Timestamp : {}----------------------".format(datetime.now()))
        os.system("ping -n 3 localhost >nul")
        os.system("echo.")
        os.system("cls")