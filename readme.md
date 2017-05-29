Finding Naturally Appealing Palettes

Having wasted many hours trying to spruce up some extremely bland wall paint, after a recent move, I decided to attack the problem another way. I created a web app where you can upload a photo and get back a visual representation of your photos’ main color palette alongside a customized set of appealing complementary color options given that palette.

I also created a unique dataset of color palettes, extracted from top nature and landscape National Geographic wallpapers, that will be used to generate the complementary color suggestions. However, any other set of photos can be easily swapped in to generate this dataset instead of National Geographic.

- Link to short presentation (starts at 6:15): https://youtu.be/jyg6dzS37PQ
- Slide deck: Presentation-Deck.pdf

My project was built in Python and primarily employed web scraping, creative data transformation techniques, DBSCAN clustering, and silhouette scoring for the validation/modeling and flask for the front-end user interface.

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
