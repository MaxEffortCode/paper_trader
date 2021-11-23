from pandas.core.frame import DataFrame
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
color = sns.color_palette()


def df_to_csv(filename, DataFrame):
    DataFrame.to_csv(filename)
    print(f"Added DataFrame to file: {filename}")
    return


def df_to_json(filename, dct):
    with open(filename, "w") as outfile:
        json.dump(dct, outfile)
    print(f"Added DataFrame to file: {filename}")
    return


def set_up_header():

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(
        'bj8Fi1rWYC_qHTszFsnc5Q', '7xdKmiTMyn-Hz9sLZQjhCag4pUSRFw')
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': 'GEEKYGAMER1134',
            'password': 'Thatnewkid!234'}
    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'Sent Anal Crawler'}
    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']
    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    resp = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    print(f"response to request: {res}")

    return headers


def get_hundred_posts(subreddit, headers):
    res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/hot",
                       headers=headers)

    df = pd.DataFrame()
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'score': post['data']['score'],
            'id': post['data']['id']
        }, ignore_index=True)

    return df


def all_posts_comments(df, headers):
    try:
        post_id_arr = df['id']
        subreddit = df['subreddit']
    except:
        print("Missing Reddit Links To Posts")
        return
    
    # Grabs the comments of each link in the data-file
    for x in range(len(post_id_arr)):
        res = requests.get(f"https://oauth.reddit.com/r/{subreddit[x]}/comments/{post_id_arr[x]}",
                       headers=headers)
        for comment in res.json()[1]['data']['children']:
            
            # if child type "kind" is comment "t1"
            if(comment['kind'] == "t1"):
                print(comment['data']['body'])
                comment_file = open("comment_file.txt","a")
                comment_file.writelines(comment['data']['body'])
                comment_file.write(f"this is the score \n\n\n\n {str(comment['data']['score'])} \n\n\n\n")
    
    return


if __name__ == '__main__':
    headers = set_up_header()
    df = get_hundred_posts("wallstreetbets", headers=headers)
    df_comment = all_posts_comments(df, headers=headers)
    df_to_csv("test.csv", df)
    # print(df.head)
    fig = px.histogram(df, x="upvote_ratio")
    fig.update_traces(marker_color="green",
                      marker_line_color='rgb(8,48,107)', marker_line_width=10)
    fig.update_layout(title_text='Up Vote to Down Vote Ratios')
    fig.show()

    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["br", "href"])
    textt = " ".join(text for text in df.title)
    wordcloud = WordCloud(stopwords=stopwords).generate(textt)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud_titles.svg', dpi=300)
    plt.show()

    textt = " ".join(text for text in df_comment.body)
    wordcloud = WordCloud(stopwords=stopwords).generate(textt)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud_comment.svg', dpi=300)
    plt.show()

    df_comment = df_comment[df_comment['score'] != 1]
    df_comment['sentiment'] = df_comment['score'].apply(
        lambda rating: +1 if rating > 1 else -1)
    print(df_comment.head())

    # split df - positive and negative sentiment:positive = df[df['sentiment'] == 1]
    negative = df_comment[df_comment['sentiment'] == -1]
    positive = df_comment[df_comment['sentiment'] == 1]

    stopwords = set(STOPWORDS)
    # good and great removed because they were included in negative sentiment
    stopwords.update(["br", "href", "good", "great"])
    pos = " ".join(review for review in positive.body)
    wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('Pos_wordcloud.png')
    plt.show()

    neg = " ".join(review for review in negative.body)
    wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
    plt.imshow(wordcloud3, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('Neg_Wordcloud.png')
    plt.show()
