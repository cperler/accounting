import datetime

from lxml import etree
from selenium.webdriver.common.by import By

from accounting.providers import OfxProvider, Statement, wait_for, wait_for_file, XPathProvider


class Chase(OfxProvider):
    def login(self, account):
        super(Chase, self).login(account)
        element = self.driver.find_element_by_id('UserID')
        element.send_keys(account.username)
        element = self.driver.find_element_by_id('Password')
        element.send_keys(account.password)
        element = self.driver.find_element_by_id('logon')
        element.click()
            
    def download(self, account):
        wait_for(self.driver, By.LINK_TEXT, 'See activity')
        return wait_for_file(self.dl_path, lambda:self.driver.get(account.download_url))

class ChaseMortgage(XPathProvider):
    def login(self, account):
        super(ChaseMortgage, self).login(account)
        element = self.driver.find_element_by_id('UserID')
        element.send_keys(account.username)
        element = self.driver.find_element_by_id('Password')
        element.send_keys(account.password)
        element = self.driver.find_element_by_id('logon')
        element.click()
    
    def download(self, account):
        wait_for(self.driver, By.PARTIAL_LINK_TEXT, account.site_key)
        self.driver.find_element_by_partial_link_text(account.site_key).click()
        
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        balance = doc.xpath("//th[text()='Principal balance']/../td/text()")[0].replace('$', '').replace(',', '')
        
        self.driver.find_element_by_partial_link_text('See transaction history').click()
        doc = etree.fromstring(self.driver.page_source, parser)
        transaction_content = doc.xpath("//div[@id='GridContainer1']//tr")[1:]

        transactions = []
        for tr in transaction_content:
            date = datetime.datetime.strptime(tr[0].text, '%m/%d/%Y')
            description = tr[1].text
            amount = tr[2].text.replace('$', '').replace(',', '')
            transactions.append({'posted':date, 'description':description, 'amount':amount})
        return Statement(account, transactions, balance)