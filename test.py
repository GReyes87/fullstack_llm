# Example usage of the SecEdgar class   
#req = SecEdgar("https://www.sec.gov/files/company_tickers.json")
#print(req.name_to_cik("Apple")) # Should return "Not Found"
#print(req.ticker_to_cik("AAPL"))
#print(req.name_to_cik("Apple Inc."))
#print(req.name_to_cik("Fake company"))  # Should return "Not Found"
#print(req.ticker_to_cik("LSHGF")) 



## Test for find_company_10Q_10K function
#result = req.name_to_cik("Apple Inc.")
#if result != "Not Found":
 #   cik = result[0]  # Extract CIK which is something like 320193
  #  submissions = req.find_company_10Q_10K(cik) ## in the function it pads the CIK and finds the 10-K and 10-Q filings for the company
   # print(submissions) ## should return a list of dictionaries with the accession number, primary document, primary doc description, form, and filing date of each 10-K and 10-Q filing
#else:
 #   print("Company not found")



# Test for annual_filing function
#print(req.annual_filing(320193,2024))                         
#print(req.annual_filing(320193,1950))    

# Test for quarterly_filing function
#print(req.quarterly_filing(1045810, 2024, 1))  # Should return the text of the 10-Q filing for Apple Inc. for Q1 2024    
#print(req.quarterly_filing(1045810, 2024, 2))  # Should return the text of the 10-Q filing for Apple Inc. for Q2 2024

