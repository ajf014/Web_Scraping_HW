from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # VISIT THE MARS.NASA.GOV WEBSITE
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the average temps
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    # MARS WEATHER
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html_weather = browser.html
    soup_weather = bs(html_weather, 'html.parser')
    mars_weather = soup_weather.find('p', class_="TweetTextSize").text

    # MARS IMAGE
    url_mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_mars_image)
    html = browser.html
    soup_mars_image = bs(html, 'html.parser')
    mars_img_path = soup_mars_image.find("img", class_='thumb')['src']
    mars_img = url_mars_image + mars_img_path



    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "mars_img": mars_img,
}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
