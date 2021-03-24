from selenium import webdriver
import datetime
import pandas as pd
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
site = driver.get("https://www.youtube.com/")
def channel_selector(channel_name, scroll_down_timer):
    timer = scroll_down_timer # in order to be able to catch as many results as you would want, decide it depending on the amount of content on the channel
    WebDriverWait(driver, 20).\
        until(EC.element_to_be_clickable((By.XPATH,
                                          '//*[@id="search"]'))).send_keys(channel_name + keys.Keys.ENTER)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer/div/div[2]/a/div[1]/ytd-channel-name/div/div/yt-formatted-string'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="icon-label"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[1]/div[2]/ytd-channel-sub-menu-renderer/div[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[1]/paper-item/tp-yt-paper-item-body/div[1]'))).click()
    while int(timer) > 0:
        driver.find_element_by_tag_name('body').send_keys(keys.Keys.END)
        timer -= 1
        time.sleep(2)
    videos_elements = driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
    return videos_elements


def parser(videos_elements):
    videos = []
    for video_element in videos_elements:
        video = {
            "title": video_element.find_element_by_xpath('.//*[@id="video-title"]').text,  # must add a dot so that it searches inside the element
            "view count": video_element.find_element_by_xpath('.//*[@id="metadata-line"]/span[1]').text,
            "uploaded since": video_element.find_element_by_xpath('.//*[@id="metadata-line"]/span[2]').text
        }
        videos.append(video)
    return videos

# using the Travellight channel for an example, and a scroll time of 5 secs


videos_items = channel_selector('Travellight', 5)
parsed_data = parser(videos_items)
df = pd.DataFrame(parsed_data)
df.to_csv("videos")
driver.quit()

