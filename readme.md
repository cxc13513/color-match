Finding Naturally Appealing Palettes

Having wasted many hours trying to spruce up some extremely bland wall paint, after a recent move, I decided to attack the problem another way. I created a web app where you can upload a photo and get back a visual representation of your photos’ main color palette alongside a customized set of appealing complementary color options given that palette.

This customization was critical, given my experience, because weeding out the irrelevant suggestions online was incredibly time-consuming and confusing. Additionally, I found many of the relevant suggestions online to be uninspiring and generic. So I decided to also create a unique dataset of color palettes, from photos online, that would be used to generate the complementary color suggestions. For me, these were top nature and landscape National Geographic wallpapers. However, I built a system that could easily use other sets of photos as well, depending on user preference.

My project was built in Python and primarily employed web scraping, creative data transformation techniques, DBSCAN clustering, and silhouette scoring for the validation/modeling and flask for the front-end user interface.


- Link to youtube of presentation (6:20 minute start): https://youtu.be/jyg6dzS37PQ
- Slide deck: Presentation-Deck.pdf


Main/helper scripts, in order need to run, in src folder:

1. Scrape photos from site & save down locally as jpegs
    - main: saved_scraped.py
    - helper:
            - scraper.py

2. Create dataset from jpegs, pickle & save locally
    - main: main_data.py
    - helpers:
            - cluster.py
            - get_colorvalues.py
            - save_scraped.py
            - transform_final.py

3. Set up locally hosted web app & user interface
    - main: webapp.py
    - helpers:    
            - main_uploaded.py
            - templates/index.html
            - templates/results.html
