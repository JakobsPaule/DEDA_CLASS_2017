# this project demonstrates webscraping on the example of LinkedIn
# the goal is to gather an overview of the german Data Science resources 
import requests
import os
from bs4 import BeautifulSoup

# import config file with credentials - path needs to be adapted
path = "C:/Users/pjakob/Documents/16_Master/DEDA/LinkedIn_Project"
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
    for i in inputs:
        try:
            if i['name'] == 'loginCsrfParam':
                csrfparamvalue = i['value']
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
   
    # Setup search parameters
    searchTerm = "blockchain"
    searchRegion = "de"
    searchString = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22" + searchRegion + "%3A0%22%5D&keywords=" + searchTerm + "&origin=FACETED_SEARCH"
    # Set range for the loop - should be dynamic
    amount = list(range(1,15))
    # Get results page for every page
    results = list()
    for i in amount:
        # paging string
        pagingString = "&page=" + str(i)
        searchURL = searchString + pagingString
        page = session.get(searchURL)
        results.append(page)


    print(len(results))
    a = session.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22de%3A0%22%5D&keywords=blockchain&origin=FACETED_SEARCH&page=1')

# Risk = Noisy Data as Strings like Headhunter would have to be excluded
# Loop over results --> results / 10 as every page has 10 results 
# page = session.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22de%3A0%22%5D&keywords=blockchain&origin=FACETED_SEARCH&page=1');
# Optional extension for the header parameters
# "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate, br","accept-language":"de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7","cookie":cookies,"referer":"https://www.linkedin.com/","upgrade-insecure-requests":1,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"})
# retrieve auth token from the 
# cookies = session.cookies.get_dict()