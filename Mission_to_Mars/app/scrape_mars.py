from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

def init_browser():

    executable_path={"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome",**executable_path, headless=False)


def scrape():
    browser=init_browser()
    listings={}

    url='https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one("ul.item_list li.slide")
    listings["Title"]= slide_elem.find("div", class_="bottom_gradient").get_text()
    listings["Description"]= slide_elem.find("div", class_="article_teaser_body").get_text()
    listings["Url"]=featured_image()
    listings["Facts"]=mars_facts()


    return listings

def featured_image():
    # Visit URL
    img_url="https://d2pn8kiwq2w21t.cloudfront.net/images/jpegPIA24487.width-1024.jpg"

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


    

