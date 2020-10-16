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
        channel='CTN9HL346',
        text = desc,
        unfurl_links = False
    )



    