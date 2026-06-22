import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}

        headers = {'user-agent': 'MLT BAS araizasierra.1@osu.edu'}
        r = requests.get(self.fileurl, headers=headers)
        r.raise_for_status()
        self.filejson = r.json()

        self.cik_json_to_dict()

    def cik_json_to_dict(self):
        for entry in self.filejson.values():
            cik = str(entry['cik_str']).zfill(10)
            ticker = entry['ticker']
            name = entry['title']

            record = (cik, name, ticker)

            self.namedict[name.lower()] = record
            self.tickerdict[ticker.upper()]= record
    
    def name_to_cik(self, name):
        return self.namedict.get(name.lower())
    def ticker_to_cik(self, ticker):
        return self.tickerdict.get(ticker.upper())
        

if __name__ == '__main__':
    se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
    print(se.ticker_to_cik('AAPL'))
    print(se.name_to_cik('Apple Inc.'))