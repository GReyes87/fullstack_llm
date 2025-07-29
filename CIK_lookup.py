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
    
    ## This functions pads the CIK with leading zeros to ensure it is 10 digits long
    def pad_cik(self, cik):
        if not cik:
            return None
        len_of_cik = len(str(cik))
        required_zeros = 10 - len_of_cik
        new_cik = '' ## Initialize new_cik as an empty string
        while required_zeros > 0:
            new_cik += '0' ## Add leading zeros if necessary
            required_zeros -= 1
        new_cik += str(cik) ## Add the original CIK after leading zeros 
        return str(new_cik) ## Return the padded CIK as a string as required by the SEC EDGAR API


    def find_company_10Q_10K(self, cik):
        ## get the submission data
        padded_cik = self.pad_cik(cik)
        if padded_cik is None:
            return "Not Found"
        url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
        headers = {'user-agent': 'MLT GR greyes2@nd.edu'}
        req = requests.get(url, headers=headers) ## Make a request to the SEC EDGAR API with the padded CIK
        self.jsonfile = req.json() if req.status_code == 200 else None ## Check if the request was successful and get the JSON data
        if self.jsonfile is None:
            return "Not Found"
        recent = self.jsonfile.get('filings', {}).get('recent', None) ## Get the recent filings from the JSON data
        if recent is None:
            return "Not Found"
        
        ## get accesion #, primary docs, and primary doc descriptions from the recent filings
        accession_numbers = recent.get('accessionNumber', [])
        primary_docs = recent.get('primaryDocument', [])
        primary_doc_descriptions = recent.get('primaryDocDescription', [])
        forms = recent.get('form', [])  
        filing_dates = recent.get('filingDate', []) 
        ## Find the 10k and 10q forms in the recent filings

        submissions = []
        for i in range(len(forms)):
            if forms[i] == '10-K' or forms[i] == '10-Q':
                submissions.append({
                    'accession_number': accession_numbers[i],
                    'primary_document': primary_docs[i],
                    'primary_doc_description': primary_doc_descriptions[i],
                    'form': forms[i],
                    'filing_date': filing_dates[i]
                })
        return submissions if submissions else "Not Found"


# Example usage of the SecEdgar class   
req = SecEdgar("https://www.sec.gov/files/company_tickers.json")
print(req.name_to_cik("Apple")) # Should return "Not Found"
print(req.ticker_to_cik("AAPL"))
print(req.name_to_cik("Apple Inc."))
print(req.name_to_cik("Fake company"))  # Should return "Not Found"
print(req.ticker_to_cik("LSHGF")) 
result = req.name_to_cik("Apple Inc.")
if result != "Not Found":
    cik = result[0]  # extract raw cik
    submissions = req.find_company_10Q_10K(cik)
    print(submissions)
else:
    print("Company not found")