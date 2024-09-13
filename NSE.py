import requests
import pandas as pd 

class IOC:
    def __init__(self,symbol,timeout=5) -> None:
        self.__url="https://www.nseindia.com/api/option-chain-indices?symbol={}".format(symbol)
        self.__session = requests.sessions.Session()
        self.__session.headers =  {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept":"*/*","Accept-Language":"en-us,en;q=0.5"}
        self.__timeout = timeout
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
    def fetch_data(self, expiry_date=None, starting_strike_price=None, number_of_rows=2):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            return data
            print(data["records"].keys())
            df = pd.json_normalize(data['records']['data'])
            if expiry_date != None:
                df = df[(df.expiryDate == expiry_date)]
            if starting_strike_price != None:
                df = df[(df.strikePrice >= starting_strike_price)][:number_of_rows]
            return df
        except Exception as ex:
            print('Error: {}'.format(ex))
            self._session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
        return []

class SOC:
    def __init__(self,symbol,timeout=5) -> None:
        self.__url="https://www.nseindia.com/api/option-chain-equities?symbol={}".format(symbol)
        self.__session = requests.sessions.Session()
        self.__session.headers =  {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept":"*/*","Accept-Language":"en-us,en;q=0.5"}
        self.__timeout = timeout
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
    def fetch_data(self, expiry_date=None, starting_strike_price=None, number_of_rows=2):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            return data
            print(data["records"].keys())
            df = pd.json_normalize(data['records']['data'])
            if expiry_date != None:
                df = df[(df.expiryDate == expiry_date)]
            if starting_strike_price != None:
                df = df[(df.strikePrice >= starting_strike_price)][:number_of_rows]
            return df
        except Exception as ex:
            print('Error: {}'.format(ex))
            self._session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
        return []

# IOC = IndexOptionChain
# SOC = StockOptionChain
