from lxml import etree
from selenium.webdriver.common.by import By

from accounting.providers import Statement, wait_for, XPathProvider


class NYCTrs(XPathProvider):
    def login(self, account):
        super(NYCTrs, self).login(account)
        self.driver.find_element_by_id("userName").send_keys(account.username)
        self.driver.find_element_by_id("userPassword").send_keys(account.password)
        self.driver.find_element_by_id("userPassword").submit()
            
    def download(self, account):
        wait_for(self.driver, By.LINK_TEXT, "Change Email")
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        amounts = doc.xpath("//div[contains(@class, 'currency')]/text()")
        total = 0.0
        for amount in amounts:
            f_amount = float(unicode(amount).encode('ascii', 'ignore').replace("$", '').replace(',',''))
            total += f_amount
        return Statement(account, [], total)
