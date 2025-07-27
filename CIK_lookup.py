import requests

class SecEdgar:
    def __init__(self,fileurl):
        ## initalizes the url, namedict, and tickerdict and data dict so that they can be used later
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}
        self.datadict = {}

        headers = {'user-agent': 'MLT GR greyes2@nd.edu'}
        ## requests the file from the url and sets the headers to identify the user agent
        r = requests.get(self.fileurl, headers=headers)

        ##  checks if the request was successful and gets the JSON data
        self.jsonfile = r.json() if r.status_code == 200 else None

        self.cik_json_to_dict() ## calls the function to populate the dictionaries


    ## This functions populates the dictionaries with the neccessary data
    ## Datadict is used to store the entire data for each CIK, namedict and tickerdict are self explanatory
    def cik_json_to_dict(self):
        if not self.jsonfile:
            return    
        self.namedict = {}
        self.tickerdict = {}
        self.datadict = {}
        for item in self.jsonfile.values():
            if not item.get('cik_str'):
                continue
            if not item.get('ticker'):
                continue
            if not item.get('title'):
                continue
            cik = item['cik_str']
            name = item['title']
            ticker = item['ticker']
            self.namedict[name.lower()] = cik
            self.tickerdict[ticker.lower()] = cik
            self.datadict[cik] = cik, name, ticker 
    ## This function returns the CIK for a given name
    def name_to_cik(self, name):
        cik = self.namedict.get(name.lower())
        if cik == None:
            return "Not Found"
        return self.datadict.get(cik, "Not Found")
    ## This function returns the CIK for a given ticker       
    def ticker_to_cik(self, ticker):
        cik = self.tickerdict.get(ticker.lower())
        if cik == None:
            return "Not Found"
        return self.datadict.get(cik, "Not Found")
    

req = SecEdgar("https://www.sec.gov/files/company_tickers.json")
print(req.name_to_cik("Apple")) # Should return "Not Found"
print(req.ticker_to_cik("AAPL"))
print(req.name_to_cik("Apple Inc."))
print(req.name_to_cik("Fake company"))  # Should return "Not Found"
print(req.ticker_to_cik("LSHGF")) 


