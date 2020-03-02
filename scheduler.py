import Atom as base
from datetime import datetime,timedelta
import time



dt = lambda x: timedelta(hours=x.hour, minutes=x.minute)

def Looper(start,end,duration = 15):
    while end > dt(datetime.now()):
        base.get_all_Nifty_csv(datetime.now())
        base.get_watch_list_csv()
        time.sleep(duration)    
    base.download_data("C:\\Users\\HP\\Desktop\\Project Golden Hen\\BhavCopy",base.BHAVCOPY_URL,"Bhavcopy_{}.zip".format(round(datetime.timestamp(datetime.now()))))
    return True


def test():
    while(True):
        print(dt(datetime.now()))
        time.sleep(60)

start = timedelta(hours=9,minutes=0)
end = timedelta(hours=16,minutes=0)
print("Collecting NSE Data ...")
Looper(start,end)
t = input()
    


