# 爬取豆瓣评分 Top250 电影
import requests
from bs4 import BeautifulSoup
import xlwt
import time
from concurrent.futures import ProcessPoolExecutor


def main(url):
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def request_douban(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')  # sheet.write(row, col, content)
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

n = 1


def save_to_excel(soup):
    movie_list = soup.find(class_='grid_view').find_all('li')
    for movie in movie_list:
        name = movie.find(class_='title').string
        img = movie.find('a').find('img').get('src')
        ranking = movie.find('em').text
        score = movie.find(class_='rating_num').string
        author = movie.find('p').text
        intro = movie.find(class_='inq').string if movie.find(class_='inq') else ''

        print('爬取电影: ' + ranking + ' | ' + name + ' | ' + img + ' | ' + score + ' | ' + author + ' | ' + intro)

        global n
        sheet.write(n, 0, name)
        sheet.write(n, 1, img)
        sheet.write(n, 2, ranking)
        sheet.write(n, 3, score)
        sheet.write(n, 4, str(author).strip())
        sheet.write(n, 5, intro)

        n += 1


if __name__ == '__main__':
    begin = time.time()
    urls = []
    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        urls.append(url)
    with ProcessPoolExecutor(4) as pool:
        pool.map(main, urls)
    book.save(u'豆瓣评分Top250电影.xls')
    end = time.time()
    print(f'{end - begin} seconds')
