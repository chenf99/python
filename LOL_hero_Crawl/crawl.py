import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')  # 禁止输出日志
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    wait = WebDriverWait(browser, 10)

    browser.get('https://lol.qq.com')
    # 先模拟滚动条往下移动，才能加载出英雄资料列表的元素 大概移动到页面2/3高度
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight/3*2)')

    heros = []

    try:
        # wait最多10s，让列表加载一会儿
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'champion-item')))
        ul = browser.find_element(By.ID, 'J_championItemContainer')
        infos = ul.find_elements_by_xpath('li')  # infos是包含148个WebElement的列表
        for info in tqdm(infos):
            hero = {}

            # 因为直接通过点击头像打开会遗漏一些页面（玄学），我选择创建新窗口
            a = info.find_element(By.CLASS_NAME, 'herf-mask').get_attribute('href')
            js = f'window.open("{a}");'
            browser.execute_script(js)
            # 切换到新打开的英雄详细信息页面
            all_h = browser.window_handles
            browser.switch_to.window(all_h[1])

            '''
            开始获取英雄详细信息
            '''
            # 获取名称
            name = browser.find_element(By.ID, 'DATAnametitle').text
            hero['name'] = name

            try:
                # 获取图片
                wait.until(EC.visibility_of_element_located((By.ID, 'skinBG')))
                img = browser.find_element(By.ID, 'skinBG').find_element_by_xpath('li').find_element_by_xpath('img').get_attribute('src')
                hero['img'] = img

                browser.execute_script('window.scrollTo(0,document.body.scrollHeight/2)')
            
                wait.until(EC.text_to_be_present_in_element((By.ID, 'DATAlore'), '。'))

                # 获取背景故事
                a = browser.find_element(By.ID, 'Gmore')
                ActionChains(browser).click(a).perform()
                background = browser.find_element(By.ID, 'DATAlore').text
                hero['backgrond'] = background

                # 获取技能介绍
                ul = browser.find_element(By.ID, 'DATAspellsNAV')
                lis = ul.find_elements_by_xpath('li')
                skills = []
                for li in lis:
                    # 切换到这个技能介绍
                    ActionChains(browser).click(li).perform()
                    skill_key = browser.find_element(By.CSS_SELECTOR, 'div.skilltitle > em').text
                    skill_title = browser.find_element(By.CSS_SELECTOR, 'div.skilltitle > h5').text
                    skill_tip = browser.find_element(By.CSS_SELECTOR, 'p.skilltip').text
                    skill = {'key': skill_key, 'title': skill_title, 'tip': skill_tip}
                    skills.append(skill)
                hero['skill'] = skills
            except TimeoutException:
                print('time out when load hero info')
            heros.append(hero)
            # 关闭当前窗口
            browser.close()
            # 切换回主页面
            browser.switch_to.window(all_h[0])
    except TimeoutException:
        print('time out when load hero list')
    print(f'total heros: {len(heros)}')
    # 写入json文件
    with open('heros.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(heros, indent=2, ensure_ascii=False))
    browser.quit()
