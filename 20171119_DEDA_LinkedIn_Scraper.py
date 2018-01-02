# this project demonstrates webscraping on the example of LinkedIn
# the goal is to gather an overview of the german Data Science resources 
import requests
import os
from bs4 import BeautifulSoup
import pandas
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# import config file with credentials - path needs to be adapted
path = "/Users/pauljakob/Docs/00_Uni/04_DEDA/Projects/DEDA_CLASS_2017_PJ"
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
    amount = list(range(1,17))
    
    # Get results page for every page and store them in an array
    results = list()
    for pageNumber in amount:
        # paging string
        pagingString = "&page=" + str(pageNumber)
        searchURL = searchString + pagingString
        print(searchURL)
        page = session.get(searchURL)
        results.append(page)
    
    # empty array where all result strings are stored
    all_cities = list()
    results_per_page = amount = list(range(1,11))
    # loop over every result page and retrieve the location
    for pages in results:
        page_soup = BeautifulSoup(pages.content, 'html.parser')
# =============================================================================
#         # code encapsulates all data
# =============================================================================
        code = page_soup.body.find_all('code')
        # the 14th code tag of each page contains the user information
        data_code = code[14].contents[0]
        # split the data string for every location 
        location_texts = data_code.split('"location":"')
        cities = list()
        # loop over locations and print out 
        for text in location_texts:
            location = text.partition(",")[0]
            print(location)
            cities.append(location)
        cities.pop(0)
        all_cities.extend(cities)
    
    # remove unnecessary information
    length = len(all_cities)
    for x in range(0, length):
        all_cities[x] = all_cities[x].replace(' und Umgebung', '')
    

    
    # get the count of each City and show a diagram for the location distribution
    loc_count = Counter(all_cities)
    loc_dataframe = pandas.DataFrame.from_dict(loc_count, orient='index').reset_index()
    loc_dataframe.columns = ['Cities', 'Talents']
    
    # plot the graph
    y_pos = np.arange(len(loc_dataframe))
    
    plt.bar(y_pos, loc_dataframe['Talents'], align='center', alpha=0.5)
    plt.xticks(y_pos, loc_dataframe['Cities'])
    plt.ylabel('Talents')
    plt.title('Blockchain Talents per city in Germany')
    plt.xticks(rotation=90)
    plt.savefig('Cities.png')
    plt.show()
    plt.savefig('Cities.pdf')