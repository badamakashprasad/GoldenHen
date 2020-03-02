import requests
import pandas as pd
import json
import csv
import os
import time
import pickle

url = "https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=AllMkt&strfilter=All"


get_name = lambda id : json.loads(requests.get("https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?Debtflag=&scripcode={}&seriesid=".format(id)).content)["Cmpname"]["FullN"]
get_industry = lambda id : json.loads(requests.get("https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode={}&seriesid=".format(id)).content)["Industry"]

data = json.loads(requests.get(url).content)['Table']
col = [i for i in data[0]]
ls = pickle.load(open("C:\\Users\\HP\\Desktop\\Project Golden Hen\\BSE_info","rb"))
#ls = {}
def make_csv(data,base_path):
    del data["PRIORITY_FLAG"]
    del data["RN"]
    del data["NSUrl"]
    del data["dt_tm"]
    del data ["index_code"]
    #ls[data["scrip_cd"]] = {'company' : get_name(data["scrip_cd"]) , 'industry' : get_industry(data["scrip_cd"])}
    #print(ls[data["scrip_cd"]])
    try:
        data["company"] = ls[data["scrip_cd"]]["company"]
        data["industry"] = ls[data["scrip_cd"]]["industry"]
    except:
        print("error in {}".format(data["scrip_cd"]))
        ls[data["scrip_cd"]] = {'company' : get_name(data["scrip_cd"]) , 'industry' : get_industry(data["scrip_cd"])}
        data["company"] = ls[data["scrip_cd"]]["company"]
        data["industry"] = ls[data["scrip_cd"]]["industry"]
    data["timestamp"] = data["FileDTTM"].replace("T"," ")
    del data["FileDTTM"]
    path = base_path + "\\" + data['scripname'].replace("*","") + ".csv"
    col = [i for i in data]
    if os.path.isfile(path):
        if data["ltradert"] not in [i["ltradert"] for i in csv.DictReader(open(path,"r",newline=""),fieldnames=col)]:
            with open(path,"+a",newline="") as fp:
                writer = csv.DictWriter(fp,fieldnames=col)
                writer.writerow(data)
                fp.close()
        else:
            pass
    else:
        with open(path,"w",newline="") as fp:
            writer = csv.DictWriter(fp,fieldnames=col)
            writer.writeheader()
            writer.writerow(data)
            fp.close()
    
    
    # open("NSE_info","wb").write(bin_)

while True:
    start = time.time()
    for i in data:
        make_csv(i,"C:\\Users\\HP\\Desktop\\Project Golden Hen\\BSE_data")
    # fp_bin = open("C:\\Users\\HP\\Desktop\\Project Golden Hen\\BSE_info","wb")
    # pickle.dump(ls,fp_bin)
    # fp_bin.close()
    print("BSE Data Retrived in {}".format(time.time() - start))