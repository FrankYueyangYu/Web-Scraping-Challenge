import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    listings={}
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
    # news 
    news_title = soup.find_all('div', class_ = 'content_title')[0].text
    news_p = soup.find_all('div', class_ = 'article_teaser_body')[0].text
    listings.update({'news_title':news_title})
    listings.update({"news_p":news_p}) 
    # Mars Featured Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url="https://spaceimages-mars.com"
    browser.visit(url)

    soup2 = bs(browser.html,'html.parser')
    i_path = soup2.find("div", class_ = "floating_text_area").find("a")
    featured_image_url = 'https://spaceimages-mars.com/'+i_path['href']

    listings.update({'featured_image_url':featured_image_url})

    # html table
    tburl="https://galaxyfacts-mars.com"
    tbl = pd.read_html(tburl)
    df = tbl[0]
    df.columns= ['Description','Mars','Earth']
    df.set_index(['Description'])
    html_tbl = df.to_html(classes="table")
    listings.update({'facts_table':html_tbl})
    html_tbl.replace("\n"," ")
    df.to_html('table.html')
    

    # hemisphere click+ dictionary
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url="https://marshemispheres.com"
    browser.visit(url)
    title=[]
    clicker = []
    img_url=[]

    soup3 = bs(browser.html,'html.parser')
    results= soup3.find_all("h3")
    clicker = [results[x].text for x in range(0,4)] 
    title = [i.strip(' Enhanced') for i in clicker]
    for x in clicker:
        browser.links.find_by_partial_text(x).click()
        time.sleep(1)
        soup4 = bs(browser.html,'html.parser')
        imglink=soup4.find("div",id="wide-image").find("a")
        img_url.append(url + imglink['href'])
        browser.back()

    hemisphere_image_urls = {
    "title":[title[0],title[1],title[2],title[3]],
    "img_url":[img_url[0],img_url[1],img_url[2],img_url[3]]}
    listings['hemisphere_image_urls']=hemisphere_image_urls

    browser.quit()

    return listings