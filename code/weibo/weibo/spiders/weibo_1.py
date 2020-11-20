import requests
from lxml import etree
import random
from openpyxl import workbook
# from abuyun import get_ip
from mysqlhelper import MysqlHelper
import time
headers = {
    'Cookie':'SCF=AjMbEg-vljqNwGAQEvlHjzNLw67gibOkHu74oNJYIjQDUi5BzrHsoQ9xjjLi1ZsfKjncTYhV273wlFaH2rpzE8o.; SUB=_2A25w50eCDeRhGeNI6FsR-SnPyD-IHXVQKGnKrDV6PUJbktANLRP-kW1NSGFVARqSA65m8QVnaCdLqq_otNotgEzj; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.7Yuiliw_.H46pUOokdZk5JpX5KzhUgL.Fo-ce0.71KM0e0e2dJLoIEqLxK-L1h-L1h.LxKqL1h5LB-2LxK.L1K.L1hqLxKMLBKqLB.ilBBtt; SUHB=0V5lNy1rfI2Lbj; _T_WM=1717b32d44fe6b93129c3fab9778851f',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    'Referer':'https://weibo.cn/search/?pos=search',
}

def proxy_pool():
    url = 'http://192.168.1.26:8088/v1/replicationpool/7fc8d49fb0344d1eb72be7d8de5f337f/key/'
    headers = {"Connection": "close"}
    res = requests.get(url, headers=headers).json()
    # res = get_proxy()
    proxy = res['data']['key']['ip:port']
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'http://{}'.format(proxy),
    }
    return proxies
def get_content(url):
    # ip1 = get_ip()
    ip_list = ['118.190.122.25:10240', '115.29.151.220:10240', '115.28.97.222:10240']
    ip = random.choice(ip_list)
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }
    # proxies = proxy_pool()
    res = requests.get(url,headers=headers)
    html = etree.HTML(res.content)
    div = html.xpath('//div[contains(@id,"M_")]')
    div_count = len(div)
    print(div_count)
    # num = 0
    for i in range(1,div_count+1):
        # 用户名
        user = html.xpath('//div[contains(@id,"M_")]['+str(i)+']//a[@class="nk"]//text()')[0]
        # user = user.encode('utf-8').decode()
        user = '人民日报'

        # 微博内容
        content = html.xpath('//div[contains(@id,"M_")]['+str(i)+']//span[@class="ctt"]//text()')
        content = ''.join(content)

        # 发布时间
        p_time = html.xpath('//div[contains(@id,"M_")]['+str(i)+']//span[@class="ct"]//text()')[0]
        p_time = p_time.strip('/xa0来自微博 weibo.com')

        # 点赞数
        zan = html.xpath('//div[contains(@id,"M_")]['+str(i)+']//a[contains(text(),"赞")]/text()')[0]
        zan = zan.encode('utf-8').decode()

        # 转发数
        zhuanfa = html.xpath('//div[contains(@id,"M_")][' + str(i) + ']//a[contains(text(),"转发")]/text()')[0]
        zhuanfa = zhuanfa.encode('utf-8').decode()

        # 评论数
        comment_num = html.xpath('//div[contains(@id,"M_")][' + str(i) + ']//a[contains(text(),"评论")]/text()')[0]
        comment_num = comment_num.encode('utf-8').decode()
        print(user)
        print(content)
        print(p_time)
        print(zan)
        print(zhuanfa)
        print(comment_num)
        # 获取评论的链接

        comment_href = html.xpath('//div[contains(@id,"M_")][' + str(i) + ']//a[contains(text(),"评论")]/@href')[0]
        print(comment_href)

        # 调用获取评论的函数
        get_comment(user,content,p_time,zan,zhuanfa,comment_num,comment_href)
        print('=='*50)
        # time.sleep(1)
    #     num += 1
    #     if num >= 1000:
    #         return
    # next_page = html.xpath('//a[contains(text(),"下页")]/@href')[0]
    # next_page = 'https://weibo.cn'+next_page
    # print('下一页：', next_page)
    # get_content(next_page)

# 获取评论
def get_comment(user,content,p_time,zan,zhuanfa,comment_num,href):
    ip = '118.190.122.25:10240'
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }
    res = requests.get(href,headers=headers)
    html = etree.HTML(res.content)
    # xpath提取评论
    try:
        comment = html.xpath('//div[contains(@id,"C_")]//span[@class="ctt"]//text()')
        comment = ''.join(comment)
    except:
        comment = ''
    print(comment)

    insert_sql = 'INSERT INTO comment(user,content,add_time,attitudes_count,reposts_count,comments_count,comment) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    data = (user, content, p_time, zan, zhuanfa, comment_num,comment)
    m.execute_insert_sql(insert_sql, data)

    # 写入excel
    ws.append([user,content,p_time,zan,zhuanfa,comment_num,comment])


if __name__ == '__main__':
    m = MysqlHelper()
    wb = workbook.Workbook()  # 创建Excel对象
    ws = wb.active  # 获取当前正在操作的表对象
    ws.append(['作者', '内容', '发布时间', '点赞数' ,'转发数' ,'评论数' ,'评论'])
    start_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E&advancedfilter=1&nick=%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5&endtime=20200303&sort=time&page={page}'
    num = 0
    for i in range(0,63):
        print('=='*50,num)
        url = start_url.format(page=i)
        get_content(url)
        num += 1
    wb.save('weibo_1.xlsx')
