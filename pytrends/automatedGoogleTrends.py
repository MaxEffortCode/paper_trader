from pytrends.request import TrendReq
import pandas as pd
import time
startTime = time.time()
pytrend = TrendReq(hl='en-GB', tz=360)

# grabs the keywords
colnames = ["keywords"]
df = pd.read_csv("pytrends\keyword_list.csv", names=colnames) # targets keyword_list.csv
df2 = df["keywords"].values.tolist()
df2.remove("Keywords")

dataset = []

# pulls trends and repeats for every keyword
for x in range(0,len(df2)):
     keywords = [df2[x]]
     pytrend.build_payload(
        kw_list=keywords,
        cat=0,
        timeframe='today 5-y', # time frame from 5 Years ago to Today
        geo='US-FL')
     data = pytrend.interest_over_time()
     if not data.empty:
          data = data.drop(labels=['isPartial'],axis='columns')
          dataset.append(data)

result = pd.concat(dataset, axis=1)
result.to_csv('pytrends\search_trends_output.csv') # pushes data out as csv

executionTime = round((time.time() - startTime), 3)
print('Execution time in sec.: ' + str(executionTime))
