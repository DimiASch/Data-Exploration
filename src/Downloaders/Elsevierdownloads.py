import pyxml2pdf.main
import requests
import os
import pandas as pd
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
#########
api_key = ''
journal_issn = ['']
#########




article_path = 'Data/articles/'
headers = {
    'Accept': 'application/json',
    'X-ELS-APIKey': api_key
    }
base_url = 'https://api.elsevier.com/content/search/scopus'
for issn in journal_issn:
    doilist = []
    authorlist = []
    yearlist = []
    start = 0
    query = f'ISSN({issn})'
    getmaxnumber = requests.get(base_url, headers=headers, params={'query': query})
    maxnumber = int(getmaxnumber.json()['search-results']['opensearch:totalResults'])
    while start < maxnumber:
        # Construct the query to get articles from a specific journal after the year 2000
        query = f'ISSN({issn})'#AND PUBYEAR < 2013
        
        # Make the request to the Scopus API
        response = requests.get(base_url, headers=headers, params={'query': query , 'start' : {start}})
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract DOIs from the response
            if  data['search-results']['opensearch:totalResults'] != 0:
                if 'search-results' in data and 'entry' in data['search-results']:
                    articles = data['search-results']['entry']
                    for article in articles:
                        #print(article)
                        if 'prism:doi' in article:
                            doilist.append(article['prism:doi'])
                            if 'dc:creator' in article:
                                authorlist.append(article['dc:creator'])
                            else:
                                authorlist.append('XXX')
                            yearlist.append(article['prism:coverDate'])
                            dirstring = article['prism:publicationName']
                        folderpath = f'{article_path}{dirstring}'
                        os.makedirs(folderpath, exist_ok=True)
                else:
                    print("No articles found or invalid response.")
                    start = maxnumber +1
        else:
            print(f"Error: {response.status_code}")
        start += 25 
        print(start)
    for doi  in doilist:
        author = authorlist[doilist.index(doi)]
        year  = yearlist[doilist.index(doi)]
        yearonly = year[0:4]
        artdirstring = yearonly + "_" + author+ doi.replace("/", "_") + ".xml"
        artpath = f'{folderpath}/{artdirstring}'
        pdf_url = f'https://api.elsevier.com/content/article/doi/doi/{doi}?apiKey={api_key}'
        pdf_response = requests.get(pdf_url)#requsts the pdf
        with open(artpath, 'wb') as file:
            file.write(pdf_response.content)
