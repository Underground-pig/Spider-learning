import requests
from lxml import etree
from jsonpath import jsonpath


class Tieba(object):
    def __init__(self, name):
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(name)
        self.proxies = {
            'http': 'http://106.13.185.186:11721',
            'https': 'https://106.13.185.186:11721'
        }
        self.headers = {
            # 请求头模拟的浏览器版本太高，导致请求返回的html文档中由注释部分，此时xpath语法识别不了
            # 两种解决办法 1.使用低版本浏览器模拟   2.对源码进行编码，将注释符删去
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            # 'User_Agent':'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0; DigExt)'
        }

    def get_data(self, url):
        """获取返回数据"""
        response = requests.get(url, headers=self.headers)


    def parse_data(self, data):
        """解析数据,返回页面信息和下一页的url"""
        # 因为高版本的请求头的返回文档中有注释，所以将注释符全部清空
        data = data.decode().replace("<!--", "").replace("-->", "")
        html = etree.HTML(data)
        li_list = html.xpath('//li[@class=" j_thread_list clearfix thread_item_box"]/div/div[2]/div[1]/div[1]/a')
        # print(len(li_list))
        page = []
        for li in li_list:
            li_info = {}
            li_info['title'] = li.xpath('./text()')[0]
            li_info['link'] = 'https://tieba.baidu.com/' + li.xpath('./@href')[0]
            page.append(li_info)
        try:
            next_url = 'https:' + html.xpath('//a[contains(text(), "下一页>")]/@href')[0]
        except:
            next_url = None
        # print(next_url)
        return page, next_url

    def save_data(self, page):
        """保存数据"""
        with open('info.txt', 'a',encoding='utf-8') as f:
            for p in page:
                f.write(p['title'])
                f.write(' : ')
                f.write(p['link'])
                f.write('\n')

    def run(self):
        """主函数"""
        url = self.url
        data = self.get_data(self.url)
        page, next_url = self.parse_data(data)
        self.save_data(page)
        while next_url is not None:
            data = self.get_data(next_url)
            page, next_url = self.parse_data(data)
            self.save_data(page)

if __name__ == '__main__':
    tieba = Tieba('孙笑川')
    tieba.run()
