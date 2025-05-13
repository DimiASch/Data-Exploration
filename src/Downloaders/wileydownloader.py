import requests
import argparse
import sys
from urllib.parse import quote_plus
from habanero import Crossref
from requests.exceptions import HTTPError
import time
import os
import json

###########
 #the issn's of the wanted journal
issn_list = [] 
matching_journal_name = []
# make sure the issn ad the journal names line up
key = "" # your api key
fromdate = "2024-12-01" #format yyyy-mm-dd
todate = "2025-01-01"   #format yyyy-mm-dd
##########


def download_pdf(doi, key,issn,name):
    # Base URL of the Wiley API
    base_url = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/"
    doi = doi['DOI']
    doi = doi.strip()
    headers = {'Wiley-TDM-Client-Token': key}
    url = base_url + quote_plus(doi)
    r = requests.get(url, allow_redirects=True, headers=headers)

    # Parse response
    if r.status_code != 200:
        if r.status_code == 403:
            print(f"Download Failed (403): Unauthorized. DOI: {doi}. Check that your API key is correct.", file=sys.stderr)
        elif r.status_code == 404:
            print(f"Download Failed (404): DOI not found. DOI: {doi}.", file=sys.stderr)
        else:
            print(f"Download Failed (http status {r.status_code}). DOI: {doi}", file=sys.stderr)
            return False
        return True
    currentpath = os.path.dirname(os.path.abspath(__file__)) #the folder where the articles should be stored
    relativepath = fr'../../data/articles/{name}/'
    articlepath = os.path.realpath(os.path.join(currentpath,relativepath))
    os.makedirs(articlepath, exist_ok=True)
    articlepath += os.path.sep
    # Name the PDF using DOI, replacing "/" with "_"
    filename = doi.replace("/", "_") + ".pdf"
    print(f"Downloaded {filename}", file=sys.stderr)
    
    with open(articlepath+filename, "wb") as fp:
        fp.write(r.content)
    return True
def main(issn,name,key,fromdate,todate):

    # Remove newline characters from DOIs
    dois = []
    dois = getdois(issn,fromdate,todate)
    counter = 1
    fuktiontest = download_pdf(dois[0],key,issn,name)
    # Download PDFs for each DOI
    while counter < len(dois):
        doi = dois[counter]
        if fuktiontest:
            funktionstest = download_pdf(doi,key,issn,name)
            counter += 1
        else: 
            time.sleep(10*60)
            doi = dois[counter-1]
            funktionstest = download_pdf(doi,key,issn,name)

def getdois(issn,fromdate,todate):
    cr = Crossref()
    filter = {
            'type': 'journal-article'#
    }

    max = 100000

    if fromdate != None:
        filter['from-print-pub-date'] = fromdate

    if todate != None:
        filter['until-print-pub-date'] = todate
    try:
        res = cr.journals(
            ids= issn,
            works = True,
            limit = 1000,
            filter = filter,
            select = "DOI",
            cursor="*",
            cursor_max=max,
        )
    except HTTPError as err:
        print(err, file = sys.stderr)
        return
         
    items = [ z['message']['items'] for z in res ]
    items = [ item for sublist in items for item in sublist ]

    if len(items) == max:
        print("Warning: DOI limit reached. Results may be incomplete.", file = sys.stderr )
    return items



for issn,name in zip(issn_list,matching_journal_name):
    if len(issn_list) != len(matching_journal_name):
        sys.exit("An error occurred: The length of the Issn and Journal Name list do not match.")
    main(issn,name,key,fromdate,todate)
