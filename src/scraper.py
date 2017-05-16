from bs4 import BeautifulSoup
import save_scraped
from urllib.request import urlopen


# only 15 links here:
url_link_list = ["http://photography.nationalgeographic.com/photography/photo-contest/2014/entries/gallery/nature-week-1", "http://photography.nationalgeographic.com/photography/photo-contest/2013/entries/gallery/nature-week-1/"]
urls_list = []
beginning = 'http://photography.nationalgeographic.com'
for item in url_link_list:
    link_open = urlopen(item)
    page = BeautifulSoup(link_open, 'html.parser')
    for link in page.findAll("a", {"class": "download wallpaper monitor"}):
        ending = link.get('href')
        combined = beginning+ending
        urls_list.append(combined)


# LATER: HOW TO FIND NUMBER OF PAGES DYNAMICALLY????
# 21 pages here, about 1000 here:
url_head = "http://photography.nationalgeographic.com/photography/photo-of-the-day/nature-weather/?page="
urls_list2 = []
beginning = 'http:'
for n in range(1, 22):
    url_link = url_head+str(n)
    link_open2 = urlopen(url_link)
    page2 = BeautifulSoup(link_open2, 'html.parser')
    for link in page2.findAll("img"):
        ending = link.get('src')
        # only save down if it's a jpg!!
        if ending.split('.')[-1] == 'jpg':
            combined = beginning+ending
            urls_list2.append(combined)


# 18 pages here, about 800 here:
url_head = "http://photography.nationalgeographic.com/photography/photo-of-the-day/landscapes/?page="
urls_list3 = []
beginning3 = 'http:'
for n in range(1, 19):
    url_link = url_head+str(n)
    link_open = urlopen(url_link)
    page = BeautifulSoup(link_open, 'html.parser')
    for link in page.findAll("img"):
        ending = link.get('src')
        # only save down if it's a jpg!!
        if ending.split('.')[-1] == 'jpg':
            combined = beginning3+ending
            urls_list3.append(combined)


# once have scraped urls:
# set folder path to save pics from natgeo urls
path = "/Users/colinbottles/Desktop/Cat/school/color-match/data/raw/"
# need to de-duplicate the links!!!!
all_list = list(set(urls_list)) + list(set(urls_list2)) + list(set(urls_list3))
print(len(all_list))
# save down de-duped list
save_scraped.save_down_pics_from_links(all_list, path)
# # saved down 15 pics from here
# save_scraped.save_down_pics_from_links(urls_list, path)
# # saved down 964 pics from here
# save_scraped.save_down_pics_from_links(urls_list2, path)
# # saved down 820 pics from here
# save_scraped.save_down_pics_from_links(urls_list3, path)
