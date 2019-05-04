from selenium import webdriver
import os
from time import sleep
from bs4 import BeautifulSoup
import urllib


def get_artists():
    url = 'https://www.wikiart.org/ru/artists-by-art-movement/abstraktsionizm#!#resultType:masonry'
    driver = webdriver.Chrome()
    driver.get(url)

    farther = True
    while farther:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            driver.find_element_by_class_name('masonry-load-more-button-wrapper').click()
        except:
            sleep(3)
            farther = False

    content_page = driver.page_source
    driver.close()

    soup = BeautifulSoup(content_page, "html5lib")

    all_names_blocks = soup.findAll("div", {"class": "artist-name"})

    artists_hrefs = []
    artists_names = []

    for name_block in all_names_blocks:
        art_name = name_block.find('a')['href']
        artists_names.append(art_name.split('/')[-1])
        art_href = 'https://www.wikiart.org' + art_name + '/all-works/text-list'
        artists_hrefs.append(art_href)

    return artists_hrefs, artists_names


def save_by_src(src, local_path):
    if '.png' in src:
        urllib.request.urlretrieve(src, local_path + '.png')
    elif '.jpg' in src:
        urllib.request.urlretrieve(src, local_path + ".jpg")
    else:
        urllib.request.urlretrieve(src, local_path + ".jpg")


def save_imgs_on_page(pic_list, artist, ignore=True):
    imgs_path = 'imgs/' + artist
    if os.path.exists(imgs_path) and ignore:
        print('%s was complite before' % imgs_path)
    else:
        os.makedirs(imgs_path, exist_ok=True)

        driver = webdriver.Chrome()
        driver.get(pic_list)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        content_page = driver.page_source
        driver.close()

        soup = BeautifulSoup(content_page, "html5lib")
        pic_links_blocks = soup.find_all('li', {"class": "painting-list-text-row"})
        pic_links = []
        for block in pic_links_blocks:
            pic_links.append('https://www.wikiart.org' + block.find('a')['href'])

        for pic_url in pic_links:
            try:
                driver = webdriver.Chrome()
                driver.get(pic_url)
                save_path = imgs_path + '/' + os.path.basename(pic_url)
                print(save_path)
                if ('абстракция' in driver.page_source) or ('Абстракционизм' in driver.page_source):
                    try:
                        print('tut')
                        driver.find_element_by_class_name('all-sizes').click()  
                        content_page = driver.page_source
                        soup = BeautifulSoup(content_page, "html5lib")
                        imgs_blocks = soup.find_all('div', {'class': 'thumbnail-item ng-scope'})
                        try:
                            src = imgs_blocks[-1].find('a')['href']
                            print(src)
                            save_by_src(src, save_path)
                        except:
                            pass
                        driver.close()
                    except:
                        print('tam')
                        src = driver.find_element_by_class_name('ms-zoom-cursor').get_attribute('src')
                        print(src)
                        save_by_src(src, save_path)
                        driver.close()
                    sleep(2)
                else:
                    driver.close()
            except Exception as ex:
                print(ex)


for pic_list, artist in zip(*get_artists()):
    save_imgs_on_page(pic_list, artist)
