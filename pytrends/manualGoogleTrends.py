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
user_keywords = []

timeframes = ['today 5-y','today 12-m','today 3-m','today 1-m']
timeframe_ref = 0



def main():
    #Call def here  
    #user_prompt(timeframe_ref,user_keywords)
    user_keywords = user_prompt_keywords()
    timeframe_ref = user_prompt_timeframe()



    #evaluate each keyword individually
    if user_keywords == []:
        for kw in all_keywords:
            keywords.append(kw)
            check_trends(kw,user_keywords,timeframe_ref)
            keywords.pop()
    else:
        for kw in user_keywords:
            keywords.append(kw)
            check_trends(kw,user_keywords,timeframe_ref)
            keywords.pop()

    print()
    reset = input('Would you like to make another trend analysis?: y/n ')
    if reset == 'y':
        main()
    else:
        print('goodbye')

#Not Used
def user_prompt(x,y):
    counter = 1
    custom_keywords = input('Would you like to use your own keywords to evaluate search trends?: y/n ')
    
    #User Prompt Exception
    while custom_keywords != 'y' and custom_keywords != 'n':
        print(exception_handler(0))
        custom_keywords = input()
    #Custom keywords added here
    while custom_keywords == 'y':
        y =+ str(input('Type in keyword ' + counter + ': '))
        counter =+ 1
        custom_keywords = input('Add another keyword? y/n')


    print('Select how far back you would like to research the trends.')
    x = int(input('1) 5 years 2) 12 months 3) 3 months 4) 1 month: ')) - 1
    #User Prompt Exception
    while x > 3 or x < 0:
        print(exception_handler(1))
        x = int(input()) - 1

    return x,y

#Timeframe Input
def user_prompt_timeframe():
    print('Select how far back you would like to research the trends.')
    try:
        x = int(input('1) 5 years 2) 12 months 3) 3 months 4) 1 month: ')) - 1
    except:
        x = -1

    #User Prompt Exception
    while x > 3 or x < 0:
        print(exception_handler(1))
        try:
            x = int(input()) - 1
        except:
            x = -1

    return x

#Keyword Input
def user_prompt_keywords():
    x = []
    counter = 0
    custom_keywords = input('Would you like to use your own keywords to evaluate search trends?: y/n ')
    
    #User Prompt Exception
    while custom_keywords != 'y' and custom_keywords != 'n':
        print(exception_handler(0))
        custom_keywords = input()
    #Custom keywords added here
    while custom_keywords == 'y':
        x.append(str(input('Type in keyword ' + str(counter + 1) + ': ')))
        counter = counter + 1
        custom_keywords = input('Add another keyword? y/n ')
        while custom_keywords != 'y' and custom_keywords != 'n':
             print(exception_handler(0))
             custom_keywords = input()

    return x


#Exception Handler Prompts
def exception_handler(a):
    switcher = {
        0: "wrong input, type y or n:  ",
        1: "wrong input, pick a number between 1 and 4:  ",
        2: "This is Case Two ",
    }
    return switcher.get(a, 'Invalid exception switch')


#Checks the trends
def check_trends(kw,user_keywords,timeframe_ref):
    print()
    pytrend.build_payload(keywords, cat=0, timeframe = timeframes[timeframe_ref],  geo='US')

    data = pytrend.interest_over_time()

    #Average interest per week over the entire time period
    mean = round(data.mean(numeric_only=True),2)

    print('The average of ' + kw + ': ' +str(mean[kw]))

    #if statment triggered if the time frame is 5 years
    if timeframe_ref == 0:
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

        #Comparison Last Year vs 5 Years ago
        if avg2 == 0:
            print('This didn\'t exist 5 years ago.')
        elif trend2 > 15:
            print('The last year interest is significantly higher compared to 5 years ago.' + ' It has changed by ' + str(trend2) + '%.')
        elif trend2 < 15:
            print('The last year interest is significantly lower compared to 5 years ago.' + ' It has changed by ' + str(trend2) + '%.')
        else:
            print('The last year interest has slightly changed compared to 5 years ago.' + ' It has changed by ' + str(trend2) + '%.')
            



main()



