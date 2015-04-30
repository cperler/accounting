import datetime
import time

from lxml import etree
from selenium.webdriver.support.ui import Select

from accounting.providers import XPathProvider, Statement


class PennLifeInsurance(XPathProvider):
    def login(self, account):
        super(PennLifeInsurance, self).login(account)
        self.driver.find_element_by_name("username").send_keys(account.username)
        self.driver.find_element_by_name("password").send_keys(account.password)
        self.driver.find_element_by_name("password").submit()
        self.driver.find_element_by_partial_link_text(account.site_key).click()
            
    def download(self, account):
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        net_cf = doc.xpath("//div[contains(text(), 'Net Cash Value')]/../../../following-sibling::td/span/text()")
        net_cf = net_cf[0].replace('$', '').replace(',', '')
    
        self.driver.find_element_by_partial_link_text('Transaction History').click()    
        select = Select(self.driver.find_element_by_id('display'))
        select.select_by_value("9")
        time.sleep(2)
        doc = etree.fromstring(self.driver.page_source, parser)
        transaction_content = doc.xpath("//span[@class='cData' or @class='cdata']/text()")
        
        transactions = []
        i = 0
        while i < len(transaction_content):
            description = transaction_content[i]
            amount = transaction_content[i+1].replace("$", "").replace(",", "")
            date = datetime.datetime.strptime(transaction_content[i+2], '%m/%d/%Y')
            transactions.append({'posted':date,
                                'description':description,
                                'amount':amount})
            i = i + 4
        return Statement(account, transactions, net_cf)