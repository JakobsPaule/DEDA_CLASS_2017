# this project demonstrates webscraping on the example of LinkedIn
# the goal is to gather an overview of the german Data Science resources 
import requests
import os
from bs4 import BeautifulSoup
import pandas
from collections import Counter

# import config file with credentials - path needs to be adapted
path = "/Users/pauljakob/Docs/00_Uni/04_DEDA/Projects/DEDA_CLASS_2017"
os.chdir(path)
from CONFIG import *

# put into routine with searchterm as input parameter
# implement more secure (proofs)

with requests.Session() as session:

    # set url for initial request and call website to create and retrieve session values
    url = 'https://www.linkedin.com/'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all input values / loop over the inputs / identify the csrftoken and get the value
    inputs = soup.find_all('input')
    for element in inputs:
        try:
            if element['name'] == 'loginCsrfParam':
                csrfparamvalue = element['value']
        except LookupError:
            print('Lookuperror')
    # set values for the login form
    loginurl = 'https://www.linkedin.com/uas/login-submit'
    username = payload['username']
    password = payload['password']
    jsenabled = "false"

    # open up the session by logging in successfully
    login_data = dict(session_key=username,session_password=password,isJsEnabled=jsenabled,loginCsrfParam=csrfparamvalue)
    session.post(loginurl,data=login_data,headers={"referer":"https://www.linkedin.com/"})

    # Setup search parameters region and search term
    searchTerm = "blockchain"
    searchRegion = "de"
    searchString = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22" + searchRegion + "%3A0%22%5D&keywords=" + searchTerm + "&origin=FACETED_SEARCH"
    # Set range for the loop - should be dynamic
    amount = list(range(1,15))
    
    # Get results page for every page and store them in an array
    results = list()
    for pageNumber in amount:
        # paging string
        pagingString = "&page=" + str(pageNumber)
        searchURL = searchString + pagingString
        page = session.get(searchURL)
        results.append(page)
    
    
    all_cities = list()
    results_per_page = amount = list(range(1,11))
    # loop over every result page and retrieve the location
    for pages in results:
        page_soup = BeautifulSoup(page.content)
# =============================================================================
#         # code encapsulates all data
# =============================================================================
        code = page_soup.body.find_all('code')
        # the 14th code tag of each page contains the user information
        data_code = code[14].contents[0]
        #split the data string for every location 
        location_texts = data_code.split('"location":"')
        cities = list()
        # loop over locations and print out 
        for text in location_texts:
            location = text.partition(",")[0]
            cities.append(location)
        cities.pop(0)
        all_cities.extend(cities)
    
    print(all_cities)
    
    # get the count of each City and show a diagram for the location distribution
    loc_count = Counter(all_cities)
    loc_dataframe = pandas.DataFrame.from_dict(loc_count, orient='index')
    loc_dataframe.plot(kind='bar')
    
    
    
# Risk = Noisy Data as Strings like Headhunter would have to be excluded
# Loop over results --> results / 10 as every page has 10 results 
# page = session.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22de%3A0%22%5D&keywords=blockchain&origin=FACETED_SEARCH&page=1');
# Optional extension for the header parameters
# "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate, br","accept-language":"de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7","cookie":cookies,"referer":"https://www.linkedin.com/","upgrade-insecure-requests":1,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"})
# retrieve auth token from the 
# cookies = session.cookies.get_dict()