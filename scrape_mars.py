# Using Jupyter notebook working code, i will turn it into scraper app to Scrape Web Data about Mars and return Library to collect all scared Data

# Importing dependencies required for entire code below
import os
import time
import shutil
import requests
import numpy
from splinter import Browser
import pandas as pd
from selenium import webdriver
from IPython.display import Image
from urllib.parse import urlsplit
from bs4 import BeautifulSoup as bs

# Initializing browser method 
def init_browser():
    # Chromdriver location
    exe_path = {"executable_path": os.path.abspath("chromedriver.exe")}
    return Browser("chrome", **exe_path, headless=False)

# initiating srapeer moethod
def scrape():
    browser = init_browser()

    # Setting up mars dictionary for all data that will be scraped from nasa websites
    mars_data = {}

    # Using browser.visit we wll visit Nasa Mars News page
    time.sleep(5)
    url ="https://mars.nasa.gov/news/"
    browser.visit(url)
    # I am placing 5s hold time in order for page to load properly
    time.sleep(5)

    webpage = browser.html
    soup = bs(webpage,"html.parser")

# Idenify the recent article and save title, and date into variables
    news_title_text = soup.find("div",class_="content_title").text
    news_paragraph_text = soup.find("div", class_="article_teaser_body").text
    mars_data['news_title'] = news_title_text
    mars_data['news_paragraph'] = news_paragraph_text

# Mars Featured Image
# Using browser.visit we wll visit Mars image
    mars_img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_img_url)
    time.sleep(5)
# Scrape the page with beautiful soup and retrive the image string:
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    mars_data["featured_image_url"] = featured_image_url

# Mars Weather
    # Visit Mars Weather Twitter address
    twt_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twt_url)
    time.sleep(5)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    m_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = m_weather

# Mars Facts
    url_facts = "https://space-facts.com/mars/"

    mars_facts_table = pd.read_html(url_facts)
    mars_facts_table[0]
    # Create columns parameter and values and set index on parameter
    df_mf = mars_facts_table[0]
    df_mf.columns = ["Parameter", "Values"]
    df_mf.set_index(["Parameter"])
    mars_html_table = df_mf.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data["mars_facts_table"] = mars_html_table

# Marsh Hemispheres
# I am going to visit the page that provides inforamtion about Mars hemispheres and collect required informations
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
# I am going to screape the page into soup and create list container mars_hem to store the data  
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hm = []
# use for loop to go through tag of each hemisphere and load data in dictionary. Since this one is challenging, 
# im going to pseudocode and write the code around the pseudo code

    for i in range (4):
        # placing the timer on 5s between each eteration through the loop    
        time.sleep(5)
        # locating images through tag h3
        images = browser.find_by_tag("h3")
        # clicking on each image to get to the correct
        images[i].click()
        # bringint into soup
        html = browser.html
        soup = bs(html, "html.parser")
        # looking into high res image
        partial = soup.find("img", class_="wide-image")["src"]
        # looking for image title
        img_title = soup.find("h2",class_="title").text
        # getting image urale
        img_url = "https://astrogeology.usgs.gov"+ partial
        # storing data into dictionary
        dictionary={"title":img_title,"img_url":img_url}
        # appending the data inot mars hemishere dictionary
        mars_hm.append(dictionary)
        browser.back()
    mars_data['mars_hm'] = mars_hm
    
     # Return the dictionary
    return mars_data




