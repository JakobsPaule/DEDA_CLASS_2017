# This is the homework for retrieving the CRIX Data directly from a website and building up a histogram

# Importing the required packages 
# request for the connection / json for parsing the result / parser to parse the date values / plt to plot the data
import requests
import json
import matplotlib.pyplot as plt
from dateutil import parser

# get the JSON Data from the website and transform to python list
response = requests.get("http://crix.hu-berlin.de/data/crix.json")
crixData = response.content
valueList = json.loads(crixData)

# create lists for x and y values
yValues = list()
xValues = list()
for i in valueList: 
    xValues.append(parser.parse(i['date']))
    yValues.append(i['price'])

# remove irregular last values and adapt the dates accordingly
while yValues[len(yValues)-1] < yValues[1]:
    yValues.pop()
    xValues.pop()

# build up a time series plot with the data
plt.plot(xValues, yValues)
plt.show()
