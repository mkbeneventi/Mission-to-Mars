from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import html5lib
import io
from zipfile import ZipFile
import urllib.request
import re
from lxml import html
from splinter import Browser
import pymongo


def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

# URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = bs(html,"html.parser")

# Retrieve elements
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    print(news_title)

    print(news_paragraph)

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

# URL of page to be scraped
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

# Retrieve elements
    featured_img= soup.find("div", class_="carousel_items").find("article")["style"]
#return with base url
    featured_image_url = f'https://www.jpl.nasa.gov{featured_img}'

    print(featured_image_url)
    
# Retrieve elements
    featured_image= soup.find("div", class_="carousel_items").find("article")["style"]
# use split function
    featured_image_split = featured_image.split("'")[1]
#return with base url
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_split}'

    print(featured_image_url)
    
# URL of page to be scraped
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    requests.get(twitter_url)
    response = requests.get(twitter_url)

# Parse HTML with Beautiful Soup
    soup = bs(response.text,"html.parser")

# Retrieve elements in text
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    print(mars_weather)

# URL of page to be scraped
    facts_url = "https://space-facts.com/mars/"

#create dataframe
    facts_df = pd.read_html(facts_url)
    facts_df = pd.DataFrame(facts_df[0])
    facts_df.head(9)



#Use Pandas to convert the data to a HTML table string.
    facts_df_html = facts_df.to_html()
    facts_df_html


# URL of page to be scraped
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    hemisphere = []
# Retrieve elements
    results = soup.find_all("div", class_="item")
# Loop through results 
    for result in results:
        hemisphere_dict = {}
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        h3 = result.find("h3").text
        href = result.find("div", class_="description").a["href"]
        title = 'https://astrogeology.usgs.gov' + href
    
        browser.visit(title)
    
    # HTML object
        html = browser.html
    # Parse HTML with Beautiful Soup
        soup = bs(html, "html.parser")
    # Retrieve elements
        url = soup.find("img", class_="wide-image")["src"]

        hemisphere_dict["title"] = h3
        hemisphere_dict["img_url"] = 'https://astrogeology.usgs.gov' + url
        print(hemisphere_dict["img_url"])
    
        hemisphere.append(hemisphere_dict)

        hemisphere

    mars_data = {
     "news_title": news_title,
     "news_paragraph": news_paragraph,
     "featured_image_url": featured_image_url ,
     "facts_df_html": facts_df_html,
     "mars_weather": mars_weather,
     "hemisphere": hemisphere
     }

    return mars_data