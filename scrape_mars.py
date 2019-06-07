def scrape():    
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import time


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    time.sleep(3)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    featured_image_url = browser.find_by_css('.fancybox-image')['src']

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    mars_weather = ''
    i = 0
    while 'InSight' not in mars_weather:
        mars_weather = browser.find_by_css('.js-tweet-text-container')[i].find_by_tag('p').text
        i += 1


    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)[0]
    mars_facts.columns = ['a','b']
    mars_facts_df = mars_facts.set_index('a')
    mars_facts_df.index.names = ['']
    mars_dict = {}
    for row in mars_facts_df.iterrows():
        mars_dict[row[0][:-1]] = row[1][0]


    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    browser.quit()
    
    dict_out = {'news_title': news_title,
                'news_p': news_p,
                'featured_image': featured_image_url,
                'mars_weather': mars_weather,
                'mars_facts': mars_dict,
                'hemisphere_imgs': hemisphere_image_urls}
    
    return dict_out