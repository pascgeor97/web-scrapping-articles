
#Import libraries
import urllib.request
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Top 10 tech articles
tech_articles = "https://medium.com/tag/tech"

# Selenium driver
browser = webdriver.Firefox(executable_path="/home/pasxgeo/selenium-firefox/drivers/geckodriver")
browser.get(tech_articles)
res = browser.execute_script("return document.documentElement.outerHTML")
browser.quit()

soup = BeautifulSoup(res, 'html.parser')

# Collect titles
title=[]
for my_tag in soup.find_all(True,{'class':['graf graf--h3 graf-after--figure graf--title','graf graf--h3 graf--leading graf--title','graf graf--h3 graf-after--figure graf--trailing graf--title','graf graf--h3 graf-after--h4 graf--trailing graf--title','graf graf--h3 graf--leading graf--title']}):
    title.append(my_tag.text)

# Collect authors
author = []
for my_tag in soup.find_all(class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken"):
    author.append(my_tag.text)

# Collect publications
publication=[]
for my_tag in soup.find_all(class_="ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal"):
    publication.append(my_tag.text)

# Collect reading time
reading_time=[] 
for my_tag in soup.find_all(class_="readingTime"):
    reading_time.append(my_tag.get('title'))

# Collect claps
claps=[]
for my_tag in soup.find_all('span',{'class':'u-relative u-background js-actionMultirecommendCount u-marginLeft5'}):
    claps.append(my_tag.text)

# Collect links
link=[]
for my_tag in soup.find_all(class_="postArticle-readMore"):
    for x in my_tag.find_all('a'):
        link.append(x.get('href'))

# Clean data
for i in range(0,len(title)):
    # Clear \xa0 from title
    title[i]=title[i].replace('\xa0',' ')
    # Keep number of minutes in reading time
    temp = reading_time[i].split(" ")
    reading_time[i] = temp[0]
    # Convert 1K to 1000
    if (claps[i][-1] == 'K'):
        claps[i]=claps[i].replace('K','')
        if ('.' in claps[i]):
            claps[i]=claps[i].replace('.','')
            claps[i] = claps[i] + "00"
        else:
            claps[i] = claps[i] + "000"

# Create dataframe
dataset = pd.DataFrame({'Title':title,'Author':author,'Publication':publication,'Reading time':reading_time,'Claps':claps,'Link':link})

print(dataset)


