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
    img_drilldown = soup_mars_image.find("img", class_='thumb')
    img_source = img_drilldown['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+img_source

#     MARS TABLE
    marsfacts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(marsfacts_url)
    tables_df = tables[0]
    tables_df.columns = ['fact', 'value']
    mars_html = tables_df.to_html(header=True, index=False)
    clean_mars_html= mars_html.replace('\n', '')

#     HEMISPHERES
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    hem_html = browser.html
    hem_soup = bs(hem_html, 'html.parser')
    hem_pics = hem_soup.find_all("img", class_='thumb')
    hem_title = hem_soup.find_all("h3")
    hemisphere_image_urls = []
    for i in range(len(hem_pics)):
            img_source = hem_pics[i].get("src")
            title = hem_title[i].text
            base_url = 'https://astrogeology.usgs.gov/'
            hemisphere_image_urls.append({"title": title, "img_urls": base_url + img_source})



    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "featured_image_url": featured_image_url,
        "clean_mars_html": clean_mars_html,
        "hemisphere_image_urls": hemisphere_image_urls
}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
