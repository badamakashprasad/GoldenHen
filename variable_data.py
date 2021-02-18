import os

HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}

PARENT_PATH = 'D:\\GoldenHen'
NSE_PATH = os.path.join(PARENT_PATH,'NSE_data')
NSE_LOG_FILE = os.path.join(PARENT_PATH,'NSE_data_log.log')
NSE_COMPANY_DATA_PATH = os.path.join(NSE_PATH,'Companies_data')
NSE_ALL_COMPANY_LIST_FILENAME = 'all_companies_list.csv'
NSE_ALL_COMPANY_LIST_URI = os.path.join(NSE_PATH,NSE_ALL_COMPANY_LIST_FILENAME)
NSE_INDICES_PATH = os.path.join(NSE_PATH,'nseJsonListing.csv')


BSE_PATH = os.path.join(PARENT_PATH,'BSE_data')
BSE_COMPANY_DATA_PATH = os.path.join(BSE_PATH,'Companies_data')


ALL_COMPANY_LIST_URL = 'https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies'
