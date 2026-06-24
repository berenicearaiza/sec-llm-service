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

    # Private helpers
    def _get_submissions(self, cik):
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        headers = {'User-Agent': 'MLT BAS araizasierra.1@osu.edu'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def _build_filing_url(self, cik, accession_number):
        accession_no_dash = accession_number.replace('-', '')
        return(
            f'https://www.sec.gov.Archives/edgar/data/{int(cik)}/'
            f'{accession_no_dash}/{accession_number}-index.htm'
        )

    # Public Methods
    def annual_filing(self, cik, year):
        submissions = self._get_submissions(cik)
        recent = submissions['filings']['recent']

        for i, form in enumerate(recent['form']):
            filing_date = recent['filingDate'][i]
            filing_year = filing_date.split('-')[0]

            if form == '10-K' and filing_year == str(year):
                accession_number = recent['accessionNumber'][i]
                url = self._build_filing_url(cik, accession_number)
                return {
                    'cik': cik,
                    'form': form,
                    'filing_date': filing_date,
                    'accession_number': accession_number,
                    'url': url
                }
        # if no filing found
        return None

    def quarterly_filing(self, cik, year, quarter):
        if quarter not in (1, 2, 3):
            raise ValueError('Quarter must be 1, 2, or 3.')

            months = {
                1: ('01', '02', '03'),
                2: ('04', '05', '06'), 
                3: ('07', '08', '09'), 
            }
            valid_months = months[quarter]

            submissions = self._get(cik)
            recent = submissions['filings']['recent']

            for i, form in enumerate(recent['form']):
                filing_date = recent['filingDate'][i]
                parts = filing_date.split('-')
                filing_year = parts[0]
                filing_month = parts[1]

                if form == '10-Q' and filing_year == str(year) and filing_month in valid_months:
                    accession_number = recent['accessionNumber'][i]
                    url = self._build_filing_url(cik, accession_number)
                    return {
                        'cik': cik,
                        'form': form,
                        'quarter': quarter,
                        'filing_date': filing_date,
                        'accession_number': accession_number,
                        'url': url
                    }

            return None




if __name__ == '__main__':
    se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
    cik, name, ticker = se.ticker_to_cik('AAPL')
    print(f'{name} | CIK: {cik}')

    annual = se.annual_filing(cik, 2023)
    print('Annual 10-K:', annual)

    quarterly = se.quarterly_filing(cik, 2023, 3)
    print('Q3 10-Q:', quarterly)

