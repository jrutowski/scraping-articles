
**Project description:** In the advent of COVID-19, many places of work have adopted the online chat rooms such as Slack, to allow their employees to communicate more efficiently. One of the upsides of Slack is that it has a convenient API which allowed me to explore its use and eventually create a bot that sends one message per day in a designated 'News' Sub-Room. The bot scrapes the news website (in our case, http://wwww.insidehighered.com and simply lists the front page articles, along with their corresponding links. This allows me to easily wake up, and read some of the latest headlines before beginning my work day. This was certainly more of a pet-project, but one that I enjoyed especially since it gave me some exposure to working with webscraping. 

The finished product will be a bot with the following output in your specified slack channel. Some future opportunities might be to create an executeable script that kicks off every day upon computer login for total automation and versatility.

<img src="http://jrutowski.github.io/scraping-articles/End%20Result%20Screenshot.PNG"/>


The code is as follows below:


```python
import requests
import urllib.request 
import time 
import pandas as pd
from bs4 import BeautifulSoup 


###################################################################################################
#Parsing the Inside Higher Education Website for the stories on the front page
###################################################################################################

#Setting the Chronicle URL to the actul website
url = ('https://www.insidehighered.com/news')
response = requests.get(url)
response #check response code

soup = BeautifulSoup(response.text, "html.parser")
one_a_tag = soup.findAll('a')

#Creating a datetime string
import datetime
now = datetime.datetime.now()
now_str = now.strftime('%A, %B %d, %Y')
date = now.strftime('%Y-%m-%d')

#Loop through--Scrape the Headline Titles and correspondinglinks
titles = soup.find_all('h3', class_ = 'views-field views-field-field-article-smarttitle')
title_list = []
link_list = []
for link in range(len(titles)):
    title_list.append(titles[link].get_text())
    link_list.append(titles[link].find("a")['href'])

#Creating the full links for inside higher ED#
url_list = []
url_title = 'http://www.insidehighered.com'
for i in range(len(link_list)):
    link = url_title+link_list[i]
    url_list.append(link)

#Create a dictionary mapping titles to the actual links
dic = {title_list[i]:url_list[i] for i in range(len(url_list))}
df = pd.DataFrame(dic.items(), columns = ['title', 'link'])


###################################################################################################
#Creating the Slack Bot
###################################################################################################

import slack
import datetime
from config import SLACK_TOKEN SLACK_CHANNEL


sc = slack.WebClient(SLACK_TOKEN)

now = datetime.datetime.now()
now_str = now.strftime('%A, %B %d, %Y')
date = now.strftime('%Y-%m-%d')
morning_statement = 'Good Morning \n Today is '+ now_str+ ' \n Here are todays top articles:'

#Sending the messages to our Slack Channel
sc.chat_postMessage(channel = SLACK_CHANNEL, text = morning_statement,)
for i in range(len(df[0:10])):
    desc = "{0} | <{1}>".format(df['title'][i], df['link'][i])
    sc.chat_postMessage(
        channel='SLACK_CHANNEL',
        text = desc,
        unfurl_links = False
    )

```

