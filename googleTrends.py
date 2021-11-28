from pytrends.request import TrendReq
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import time
import datetime
from datetime import datetime, date, time


pytrend = TrendReq(hl='en-US', tz=360)

all_keywords = ['msft','sony','aapl','amzn']

keywords = []

timeframes = ['today 5-y','today 12-m','today 3-m','today 1-m']
print('Select how far back you would like to research the trends.')
x = int(input('1) 5 years 2) 12 months 3) 3 months 4) 1 month: ')) - 1

while x > 3 or x < 0:
    x = int(input('ok ret**d, pick a number between 1 and 4: ')) - 1

#Checks the trends
def check_trends():
    pytrend.build_payload(keywords, cat=0, timeframe = timeframes[x],  geo='US')


    data = pytrend.interest_over_time()
    #print(data)

    #Average interest per week over the entire time period
    mean = round(data.mean(numeric_only=True),2)

    print('The average of ' + kw + ': ' +str(mean[kw]))
    #if statment triggered if the time frame is 5 years
    if x == 0:
        #avg for the most recent year
        avg = round(data[kw][-52:].mean(),2)
        #avg for the first year starting five years ago
        avg2 = round(data[kw][:52].mean(),2)
        #trend indicates the percentage increase or decrease of interest over the last year
        trend = round(((avg/mean[kw])-1)*100,2)
        trend2 = round(((avg/avg2)-1)*100,2)
        print('The last year interest of ' + kw + ' compared to the last 5 years ' + 'has changed by ' + str(trend) + '%.')
        
        # Stable Trend Evaluation
        if mean[kw] > 75 and abs(trend) <= 5:
            print('The interest for ' + kw + ' is stable in the last 5 years.')
        elif mean[kw] > 75 and trend > 5:
            print('The interest for ' + kw + ' is stable and increasing in the last 5 years')
        elif mean[kw] > 75 and trend < -5:
            print('The interest for ' + kw + ' is stable and decreasing in the last 5 years')
        
        # Relatively Stable Trend Evaluation
        elif mean[kw] > 60 and abs(trend) <= 5:
            print('The interest for ' + kw + 'is relatively is stable in the last 5 years.')
        elif mean[kw] > 60 and trend > 5:
            print('The interest for ' + kw + ' is relatively stable and increasing in the last 5 years')
        elif mean[kw] > 60 and trend < -5:
            print('The interest for ' + kw + ' is relatively stable and decreasing in the last 5 years')

        # Seasonal, Substational changes?
        elif mean[kw] > 20 and abs(trend) <= 15:
            print('The interest for ' + kw + ' is seasonal.')
        #Increasing Interest
        elif mean[kw] > 20 and trend > 15:
            print('The interest for ' + kw + ' is significantly trending.')
        #Declining interest
        elif mean[kw] > 20 and trend < -15:
            print('The interest for ' + kw + ' is significantly decreasing.')
        #New and Trending
        elif mean[kw] > 0 and trend > 15:
            print('The interest for ' + kw + 'is new and trending.')

        # Other
        else:
            print('Trend Evaluation needs to be refined')


#evaluate each keyword individually
for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()

