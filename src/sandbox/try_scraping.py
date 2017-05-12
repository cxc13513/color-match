from bs4 import BeautifulSoup
import re
import requests

# useful resources:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors

# need to get list of all years of photography nature/landscape contests
# cuz it's different every year!
photo_url = 'http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/gallery/week-10-landscape/1'
contents = requests.get(recipes_url).content
soups = BeautifulSoup(contents, 'html.parser')
urls_list = soups.select('li > a')
#return scrubbed urls_list

#need to scrub urls_list to get links to webpage for each recipe type, where there will be individual links to actual recipes
#once scrubbed, can just go over it in a for loop with code below.

scrubbed_urls_list = 'https://smittenkitchen.com/recipes/appetizers-party-snacks/?format=list'
def get_indiv_urls_from_type(scrubbed_urls_list):
    scrubbed_indiv_urls = []
    for i in range(len(scrubbed_urls_list)):
        contentz = requests.get(scrubbed_urls_list[i]).content
        soupz = BeautifulSoup(contentz, 'html.parser')
        indiv_urls = soupz.select('li > a')
        #need to clean indiv_urls....probably do this in another function
        for j in range(len(indiv_urls)):
            indiv = re.compile(r"\https://smittenkitchen.com/""+/d+[a-zA-Z]+[]+, indiv_urls[j])


        scrubbed_indiv_urls.append(indiv_urls_clean)
    #return scrubbed indiv_urls


#need to scrub indiv_urls to get links to actual recipes!
#once scrubbed, can just go over it with a for loop below to get text of recipe, text of comments, and text of categorization, if possible.











live_url = 'https://smittenkitchen.com/2017/03/black-lentil-dal/'
content = requests.get(live_url).content
soup = BeautifulSoup(content, 'html.parser')

#pull out recipe text
recipe_p_tags = soup.select('.entry-content')
texts = [tag.text for tag in recipe_p_tags]
full_text = ' '.join(texts)

#pull out comments
comment_p_tags = soup.select('.comment-content')

#pull out categories for recipe
categories_p_tags = soup.select('.cat-links')
