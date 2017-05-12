from bs4 import BeautifulSoup
from lxml import html
import os
import pdb
import save_scraped
from selenium import webdriver
import sys
from urllib.request import urlopen

driver = webdriver.Chrome()
url = 'http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/wallpapers/winners-landscape/1'
driver.get(url)
driver.page_source.encode('utf-8')
driver.find_element_by_class_name("#ys-carousel-inner > div:nth-child(1) > img")
driver.find_element_by_xpath("//*[@id='ys-carousel-inner']/div[1]/img")
//*[@id="ys-carousel-inner"]/div[3]/img
outer_ele
selector = #ys-carousel-inner > div:nth-child(1) > img
//*[@id="ys-carousel-inner"]/div[1]
element = <img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-FwsgxqjzBayK9qESNghf2eWScFYc_P2xP2ImNHJHsVVOica0l/" draggable="false" alt="Blood Moon Eclipse and Old Faithful " style="width: 495px; height: auto;">

content = driver.find_element_by_css_selector('div.ys-carousel-item')
driver.find_element_by_id('loginForm')


## You have to switch to the iframe like so: ##
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
xpath_parent1 = "//*[@id='ys-carousel-inner']"
elem = driver.find_element_by_xpath(xpath_parent1)
xpath_parent2 = "//*[@id='ys-carousel-inner']/div[1]"
x_path_child = "//*[@id='ys-carousel-inner']/div[1]/img"
## Insert text via xpath ##
elem = driver.find_element_by_xpath("/html/body/p")
elem.send_keys("Lorem Ipsum")
## Switch back to the "default content" (that is, out of the iframes) ##
driver.switch_to_default_content()




driver.quit()

# UGH HOW DO I GET THESE?!?!?!??!
# Take this class for granted.Just use result of rendering.
class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

url = 'http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/wallpapers/winners-landscape/1'
r = Render(url)
result = r.frame.toHtml()
#This step is important.Converting QString to Ascii for lxml to process
archive_links = html.fromstring(str(result.toAscii()))
print archive_links

pdb.set_trace()

link = 'http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/wallpapers/winners-landscape/1'
link_open = urlopen(link)
page = BeautifulSoup(link_open, 'html.parser')
temp = page.findAll("div")

'''ITS IN HERE!!!!! //yourshot under src!!! BUT HOW PULL OUT?????

"photo": {"text": "uploads/member/910883/yourshot-910883-8320585.jpg", "href": "/photos/8320585/", "src": "//yourshot.nationalgeographic.com/u/fQYSUbVfts-T7odkrFJckdiFeHvab0GWOfzhj7tYdC0uglagsDq_MMAoULm7RcJOsf9SFR-vzZr_mDUvIDDSYUBjRKYAncGnBPFAgPHCLExkT39LyQwaQgT5ddp1th5KBp8iqTUwVWQiESXkR-7rG8MJHXUjVb_IbbAAXUtgAskxNU5gPpI4qGuqzQ8JW64hzdZE_dzOWrY8aRt5ilifXFMGkmM/"}
'''

'''
<div class="ys-carousel-inner animating" id="ys-carousel-inner" style="width: 9405px; height: 427.938px; transform: translate3d(-15.7895%, 0px, 0px) scale3d(1, 1, 1);"><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-FwsgxqjzBayK9qESNghf2eWScFYDIf02Uf3tYCsuRsnjoNoGpiA/" draggable="false" alt="Blood Moon Eclipse and Old Faithful " style="width: 495px; height: auto;">

<span class="ys-carousel-control--behind ys-carousel-control--left" role="button"></span>
<span class="ys-carousel-control--behind ys-carousel-control--right" role="button"></span>

</div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z27yhN-ocZEYR3O2Cgod-Fs4CUO5_TU1F1eXsA9_wQIw/" draggable="false" alt="Reverie" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z37V_knd8IpA-HxlsO8T6eIcb2uoJtaUni6v8XLO5BDQ/" draggable="false" alt="Life Among Death" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z1Ru-d-onnB7zFOj73Q0JZNR_HhXN-QA6YKJrIhiVADg/" draggable="false" alt="Fracturing Icecap" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z246Rym4Z5Ru9qPhlEMRS__Fsu5PpziLm_DDan3sx-KQ/" draggable="false" alt="Mars" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z37C2NUWNUoXWi01kZ_7vZGzp65k0iNoIlp9S78cBxQQ/" draggable="false" alt="Orange Dawn" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z24EyIgRcCpDUoUP247k9vGXmLnoq9pKnGpcKF0zysYA/" draggable="false" alt="The Starry Night in Real World" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z1SE6xivxliX51ggGsGr88dvrIk0pvMIPfh56dhckrpA/" draggable="false" alt="Herculean stove" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z27glnLwIqXGbXgGNGdjhd6kAuEznt9LN-dlNxahlIZw/" draggable="false" alt="Morning Glory Hot Spring in Yellowstone" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z25T21bH43kOa-JGmigTMUhrDDCBrJnFku4lodU7loeA/" draggable="false" alt="Old and new" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z25TVjJiEAml-o2r8v2eNYPOoeSh0rWlubLBiJx25uQA/" draggable="false" alt="Hverfjall Tephra Cone" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z246_3xZhfk3UenrGHCg0nFhLVy0EzFlj174RFFgIDMA/" draggable="false" alt="The Fairy and the Goblins" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z1R_gg5UOUCF0bXZcKzGbRY3QJQl-HzaU2RPd3FXh2-g/" draggable="false" alt="The Glowworm Passageway" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq09ZmX-csxfDv1OEr_NgWq6SCWD7iwEdwHj1lkNg5ORmoQ/" draggable="false" alt="Serendipitous Green Meteor" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z27yngIiaHsY6FLkJCHUCs18DCzCpOPGzMH3eE6MBQjQ/" draggable="false" alt="The Beginning" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z24WzMVDaHGVSCHomnP9Jxn_GOjGSoli76LEHt4sHtXw/" draggable="false" alt="Planet’s fiery breathe " style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z24jnw6LgkZRmSzBIgVkdGDESKK9y2g6HsZUl2X3p-0Q/" draggable="false" alt="Great Wall in the Morning" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z1R_cum37J3I_Zw4YjYKX6yZ1YTcgoRtOLhbLF8Q2LHg/" draggable="false" alt="Unseen Cordilleras" style="width: 495px; height: auto;"></div><div class="ys-carousel-item" style="width: 495px; height: 427.938px;"><img src="//yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-Fwsgxq0z27yxx8Vp3Yh8bxDfnDmwmn7U3gVyEsPWEI0NY-tNyEA/" draggable="false" alt="Cracker" style="width: 495px; height: auto;"></div></div>

'''



# url4 = "https://www.instagram.com/natgeoyourshot/?hl=en"
# openlink = urlopen(url4)
# page = BeautifulSoup(openlink, 'html.parser')





# # ATTEMPT #2
# from bs4 import BeautifulSoup
# import os
# from PIL import Image
# import requests
# from selenium import webdriver
# from urllib.request import urlopen
# # set driver to be phantomjs
# driver = webdriver.PhantomJS()
# # open url of page want
# driver.get('http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/wallpapers/winners-landscape/1')
# raw_s = driver.page_source
# # feed rendered HTML in driver.page_source into BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# js_text = soup.find('script', type="text/javascript").text
# image_src = driver.find_element_by_tag_name('link')
# response = requests.get(image_src).content
# # find all links in s
# links = s.select('.src')
#
# # ATTEMPT #3
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# import requests
# link = 'http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/wallpapers/winners-landscape/1'
# driver = webdriver.PhantomJS()
# driver.get(link)
# wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[starts-with(@id, 'xdm_default')]")))
# image_src = driver.find_element_by_tag_name('img').get_attribute('src')
# response = requests.get(image_src).content
# with open('C:\\Users\\You\\Desktop\\Image.jpeg', 'wb') as f:
#     f.write(response)
# http://stackoverflow.com/questions/36993962/installing-phantomjs-on-mac






# useful resources:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors
# need to get list of all years of photography nature/landscape contests
# cuz it's different every year!

# contents = requests.get(photo_url).content
# soups = BeautifulSoup(contents, 'html.parser')
# urls_list = soups.select('li > a')

# This is what i want:
'''
<!-- BASE PHOTOCONTEST & CONTEST SPECIFIC CSS -->
<link href="//yourshot.nationalgeographic.com/static/asset-cache/photocontest.min.0b927d4b.css" rel="stylesheet" type="text/css"/>
<link href="//yourshot.nationalgeographic.com/static/asset-cache/theme-ngpc.min.1eaf007b.css" rel="stylesheet" type="text/css"/>
<link href="//assets.ngeo.com/modules-global-nav/latest/dist/styles/main.css" rel="stylesheet">
<link href="//yourshot.nationalgeographic.com/static/asset-cache/photocontest.gn.min.241e142d.css" rel="stylesheet" type="text/css"/>
'''
