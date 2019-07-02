import selenium
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm, trange
import json


def search():
    try:
        search_box = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search > div.search-m > div.form > input.text')))
        search_box.send_keys('无线耳机')
        search_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div.search-m > div.form > button.button')))
        search_btn.click()
    except TimeoutException:
        search()


def next_page(page):
    try:
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page)))
        get_img_url()
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.pn-next')))
        next_btn.click()
    except TimeoutException:
        browser.refresh()
        next_page(page)


def get_img_url():
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all(class_='gl-item')
    global count
    for item in items:
        url = dict()
        # title = item.find(class_='p-name p-name-type-2').find('a').get('title')
        # url['title'] = title
        url['title'] = str(count + 1)
        if item.find('img').get('src'):
            url['src'] = item.find('img').get('src')
        else:
            url['src'] = item.find('img').get('data-lazy-img')
        url['src'] = 'http:' + url['src']
        count += 1
        # print(url)
        urls.append(url)


def download_img():
    os.makedirs('./img/', exist_ok=True)
    for url in tqdm(urls):
        r = requests.get(url['src'], stream=True)
        with open('./img/' + url['title'] + '.jpg', 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)


if __name__ == "__main__":
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = selenium.webdriver.Chrome(options=options)
    WAIT = WebDriverWait(browser, 10)
    browser.maximize_window()
    browser.get('https://www.jd.com/')

    search()

    all_h = browser.window_handles
    browser.switch_to.window(all_h[-1])

    total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em > b'))).text
    print(total)

    urls = []
    count = 0

    print('get urls:')
    for page in trange(1, int(total) + 1):
        next_page(page)
    with open('urls.json', 'w') as f:
        f.write(json.dumps(urls))

    print('download images:')
    download_img()

    browser.quit()
