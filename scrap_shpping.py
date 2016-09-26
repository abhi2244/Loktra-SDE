'''
Created on 24-Sep-2016

@author: abhishek
'''


#!/usr/bin/python


from bs4 import BeautifulSoup
import sys, urllib2, random, time, json, re
from twisted.python.util import println
import requests



KEYWORD = 'http://www.shopping.com/products?KW={keyword}'
PAGE = 'http://www.shopping.com/products~PG-{page_num}?KW={keyword}'


def print_items(items):
    if len(items) == 0:
        print "No results for this page"
        return

    for item in items:
        print''
        print '  Item    : {}'.format(item.get('name', '').encode('utf-8').strip())
        print '  Price   : {}'.format(item.get('price', '').encode('utf-8').strip())
        print '  Merchant: {}'.format(item.get('merchant', '').encode('utf-8').strip())

class ShoppingCrawler(object):

    def total_item_count(self, keyword):
        '''
        It will count total items by calculating total pages-1 * maximum item on page +items listed on last page
        '''
        search_results = requests.get(KEYWORD.format(keyword=keyword))
        if search_results.status_code != 200:
            raise ValueError("There is no item for this keyword")

        soup = BeautifulSoup(search_results.text, 'html.parser')

        links = filter(lambda e: e.attrs.get('name') and e.attrs.get('name') != 'PLN',soup.select('.paginationNew a')) #PLN is having items no attribute

        num = [self.get_page_num(each.attrs.get('href', '')) for each in links ]
        no_of_pages = max(num) if len(num) > 0 else 0
        
        print"tatal no of pages are "+repr(no_of_pages)
        
        item_count = len(self.page_items(keyword, 1)) #items on each page 
        last_item_count = len(self.page_items(keyword, no_of_pages)) #items on last page

        return item_count * (no_of_pages-1) + last_item_count


    def get_page_num(self, link):
        res = re.search(r'PG-(?P<page_no>\d+)', link)
        try:
            return int(res.group('page_no')) if res else 0
        except ValueError:
            return 0


    def page_items(self, keyword, page):
        '''
        Page items are products for sale. These are <div>'s of class 'gridBox'
        '''
        p = requests.get(PAGE.format(page_num=page, keyword=keyword))
        if p.status_code != 200:
            raise ValueError("There is no item for this keyword or page no is out of range")
        soup = BeautifulSoup(p.text, 'html.parser')
        return soup.select('.gridBox')


    def total_items_page(self, keyword, page):
        '''
        It will count max item on page.
        '''
        items = []

        for i in self.page_items(keyword, page):
            p = i.select_one('.gridItemBtm')
            if p:
                p_name = p.select_one('.productName')
                if p_name:
                    name = p_name.attrs.get('title') or\
                            p_name.select_one('span').attrs.get('title')
                
                p_price = p.select_one('.productPrice')
                if p_price:
                    price = p_price.string or\
                            p_price.select_one('a').string

                p_merchant = p.select_one('.newMerchantName')
                if p_merchant:
                    merchant_name = p_merchant.string or\
                                    p_merchant.select_one('a').string
                if p_name and price and merchant_name:
                    items.append({
                        'name': name, 'price': price, 'merchant': merchant_name
                    })
        
        #print len(items)
        return items



if __name__ == '__main__':
    key_word=raw_input()

    crawler = ShoppingCrawler()
    print "Total no of results for "+key_word+" is {}".format(crawler.total_item_count(key_word))
    
    print""
    print"choose pages from given range"
    page_num=raw_input()
    print_items(crawler.total_items_page(key_word, page_num))