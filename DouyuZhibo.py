from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import time


class Douyu(object):

    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        options = ChromeOptions()
        options.add_argument('--headless')
        self.browse = webdriver.Chrome(service=Service('D:\Program Files\Google\Chrome\Application\chromedriver.exe'),
                                       options=options)

        pass

    def parse_data(self):
        el_room_list = self.browse.find_elements(By.XPATH, '//*[@id="listAll"]/section[2]/div[2]/ul/li')
        # print(len(el_room_list))
        # 遍历房间列表，从节点中获取数据
        for i in range(len(el_room_list)):
            room = el_room_list[i]
            # 这里只能获得第一个直播间的图片，之后就会报‘无法定位到图片相关的元素’的异常，可能是网站相关的反爬， 暂时还没头绪
            # room_info['url'] = room.find_element(By.XPATH, './div/a[1]/div[1]/div[1]/picture/img').get_attribute('src')
            with open('douyu_info.txt', 'a', encoding='utf-8') as f:
                f.write('-----------------------------------------------------------\n')
                f.write('* 标题： ' + room.find_element(By.XPATH, './div/a[1]/div[2]/div[1]/h3').text + '\n')
                f.write('* 分类： ' + room.find_element(By.XPATH, './div/a[1]/div[2]/div[1]/span').text + '\n')
                f.write('* 主播： ' + room.find_element(By.XPATH, './div/a[1]/div[2]/div[2]/h2/div').text + '\n')
                f.write('* 人气： ' + room.find_element(By.XPATH, './div/a[1]/div[2]/div[2]/span').text + '\n')
                f.write('* 简介： ' + room.find_element(By.XPATH, './div/a[1]/div[2]/span').text + '\n')

            # selenium 获得的element对象是元素在dom树上的索引或者句柄
            # 当根据该索引对元素进行操作时，会导致dom树上的其他元素的索引改变 ？ 疑问
            # 于是，如果没有重新获取element对象，就利用其他索引操作的话
            # 会报 “该元素未挂载到dom树” 的错误
            # 所以在这里要重新获取元素列表，更新索引
            # 并且重新获取前还要等待一段时间，让索引完全更新完毕
            # 具体原理还没有获悉，待更新
            time.sleep(0.3)
            el_room_list = self.browse.find_elements(By.XPATH, '//*[@id="listAll"]/section[2]/div[2]/ul/li')


    def run(self):
        self.browse.get(self.url)
        time.sleep(1)
        self.parse_data()
        while True:
            try:
                self.browse.execute_script('scrollTo(0, 10000)')
                # 滚轮移到最底部后，不能立即定位元素，因为网页可能没有渲染完成
                time.sleep(1)
                el_next = self.browse.find_element(By.XPATH, '//*[contains(text(), "下一页")]')
                el_next.click()
                time.sleep(1)
                self.parse_data()
            except:
                break

        self.browse.quit()
        pass


if __name__ == '__main__':
    douyu = Douyu()
    douyu.run()
