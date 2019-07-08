# 刷csdn阅读量的脚本
import requests
from bs4 import BeautifulSoup
import time
from tqdm import trange
import click
from concurrent.futures import ProcessPoolExecutor


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
           'Cookie': 'xxx'}


def getPage(page_url, urls):
    html = requests.get(page_url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    blog_list = soup.find(class_='article-list').find_all(class_='article-item-box csdn-tracking-statistics')
    for blog in blog_list:
        url = blog.find('h4').find('a').get('href')
        if 'chenf1999' not in url:
            continue
        print(url)
        urls.append(url)
        _ = requests.get(url, headers=headers)
        time.sleep(1)


def requestURL(url):
    _ = requests.get(url, headers=headers)
    time.sleep(1)


@click.command()
@click.option('--times', '-t', type=int, default=100, help='set read times')
def main(times):
    urls = []
    for page in range(1, 3):
        getPage(f'https://blog.csdn.net/chenf1999/article/list/{page}?', urls)
    for _ in trange(times):
        with ProcessPoolExecutor(4) as pool:
            pool.map(requestURL, urls)


if __name__ == "__main__":
    main()
