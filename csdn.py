# 刷csdn阅读量的脚本
import requests
from bs4 import BeautifulSoup
import time
from tqdm import trange
import click
from concurrent.futures import ProcessPoolExecutor


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
           'Cookie': 'smidV2=2018071901102072998cbd457437f7d263adf5cbc0e2a00027dda6a0d7259a0; UN=chenf1999; __yadk_uid=aozkHf6A8ffPlAt5k5L6f1jX0boD771b; ARK_ID=JS6584689b0f74595ae091a995d6649ba66584; uuid_tt_dd=10_28867322980-1540723154624-645938; _ga=GA1.2.342502353.1541725812; ADHOC_MEMBERSHIP_CLIENT_ID1.0=7914ff1b-833e-030c-f59b-67fcf6dc793e; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC!5744*1*chenf1999!6525*1*10_28867322980-1540723154624-645938; CNZZDATA1259587897=994393162-1552035840-https%253A%252F%252Fwww.baidu.com%252F%7C1555810756; UM_distinctid=16b36029f418d-05a6ffdbd8a3d6-37c153e-100200-16b36029f422c5; acw_tc=276082a615621351898766904efee201563bcb8abba7b669dd21917c1c286d; firstDie=1; dc_session_id=10_1562481703755.435201; UserName=chenf1999; UserInfo=da7fe7e18d6d45568ca7417b676d3515; UserToken=da7fe7e18d6d45568ca7417b676d3515; UserNick=GGBobbb; AU=D04; BT=1562482680407; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FarticleList%252Flist%22%2C%22tid%22%3A%22b83dee7654da64%22%2C%22q%22%3A0%2C%22a%22%3A37%7D; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1562501172,1562501799,1562501822,1562502101; dc_tos=pu9vji; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1562503666'}


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
