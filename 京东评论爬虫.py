from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from urllib.parse import quote,unquote
import re,json,codecs

#获取单页搜索结果的评论
def get_some_comments(search_link,keyword):
    driver = webdriver.PhantomJS(executable_path='phantomjs')
    driver.get(search_link)
    js = "var q=document.body.scrollTop=100000"
    xx = u'<li data-sku="(.*?)"\s+class="gl-item">'
    pattern = re.compile(xx)
    try:
        driver.execute_script(js)
        element = WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "J_scroll_loading")))
    
    finally:
        pageSource = driver.page_source
        good_ids = pattern.findall(pageSource)
        count_all = 0
        for good_id in good_ids:
            print(good_id)
            count = get_review(good_id,10,keyword)
            count_all += count
        driver.close()
        return count_all

#获取单个商品的评论
def get_review(good_id,page_num,keyword):
    output_data = codecs.open(''+str(unquote(keyword))+'.txt','a','utf8')
    count = 0
    for page in range(0,page_num):
        url = 'http://s.club.jd.com/productpage/p-'+good_id+'-s-0-t-3-p-'+str(page)+'.html'
        html = urlopen(url).read()
        data = json.loads(html.decode('gbk','ignore'))
        for each in data['comments']:
            count+= 1
            output_data.write(each['content'] + '\n')    
    return count

#获取@para search_page_num个页面中所有结果的商品评论
def get_many_comments(search_page_num,keyword):
    amount_all = 0
    for search_page in range(1,search_page_num+1):
        print(search_page)
        amount = get_some_comments('http://search.jd.com/Search?keyword='+str(keyword)+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sttr=1&page='+str(search_page)+'&click=0',keyword)
        amount_all += amount
    return amount_all

def parse_keyword(keyword):
    keyword = quote(word.encode('utf8'))
    return keyword

words = input('keywords: ')
for word in words.split(' '):
    print(str(get_many_comments(6,parse_keyword(word))))
