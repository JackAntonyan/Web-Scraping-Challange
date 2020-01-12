from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser ('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
    time.sleep(1)
    
    # Nasa Mars News
    
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').text
    
    news_p = soup.find('div', class_='article_teaser_body').text
    
    #Featured Image
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #stuff = soup.find('div', class_='carousel_container')
    
    image_href = soup.find('a', class_="button fancybox")["data-fancybox-href"]
    
    url = "https://www.jpl.nasa.gov/"
    featured_image_url = url+image_href    
    
    #Mars Weather from Twitter
    
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    twitter_mars_weather =soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    #Mars Space Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    tables = pd.read_html(facts_url)
    
    mars_df=tables[1]
    mars_df.columns["description", "value"]
    mars_df.set_index("description",inplace=True)
    
    mars_html_table = mars_df.to_html()
    final_html_table = mars_html_table.replace('\n',' ')
    
    #Mars Hemispheres
    
    hemi_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    all_hemispheres = soup.find('div', class_="collapsible results")
    
    hemispheres=all_hemispheres.find_all('a')
    
    hemisphere_image_urls=[]
    for hemi in hemispheres:
        if hemi.h3:
            title=hemi.h3.text
            link=hemi["href"]
            main_url="https://astrogeology.usgs.gov/"
            forward_url=main_url+link
            browser.visit(forward_url)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemi2=soup.find("div",class_= "downloads")
            image=hemi2.ul.a["href"]
            hemi_dict={}
            hemi_dict["title"]=title
            hemi_dict["img_url"]=image
            hemisphere_image_urls.append(hemi_dict)
            browser.back()
    
    mars_py_dict = {
        "mars_news_title": news_title,
        "mars_news_paragraph": news_p,
        "mars_featured_image": featured_image_url,
        "mars_weather": twitter_mars_weather,
        "mars_facts": final_html_table,
        "mars_hemisphers": hemisphere_image_urls
    }
    browser.quit()
    
    return mars_py_dict
    