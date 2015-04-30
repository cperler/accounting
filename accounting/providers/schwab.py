import csv
import datetime
import time

from lxml import etree
from selenium.webdriver.common.by import By

from accounting.providers import Statement, wait_for, wait_for_file, CSVProvider


class Schwab(CSVProvider):
    def login(self, account):
        super(Schwab, self).login(account)
        time.sleep(2)
        self.driver.find_element_by_id("SignonAccountNumber").send_keys(account.username)
        self.driver.find_element_by_id("SignonPassword").send_keys(account.password)
        self.driver.find_element_by_id("SignonPassword").submit()
        
    def download(self, account):
        self.driver.get("https://client.schwab.com/secure/cc/accounts/balances")
        self.driver.find_element_by_id("accountSelector").click()
        wait_for(self.driver, By.PARTIAL_LINK_TEXT, account.site_key)
        self.driver.find_element_by_partial_link_text(account.site_key).click()
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        balance = doc.xpath('//*[text()="Total"]/../following-sibling::td/*/text()')
        balance = balance[0].replace('$', '').replace(',', '')
        self._statement = Statement(account, [], balance)
        time.sleep(2)
        self.driver.get("https://client.schwab.com/secure/cc/accounts/history")
        self.driver.find_element_by_id("accountSelector").click()
        wait_for(self.driver, By.PARTIAL_LINK_TEXT, account.site_key)
        self.driver.find_element_by_partial_link_text(account.site_key).click()
        wait_for(self.driver, By.LINK_TEXT, "Edit Filter")
        self.driver.find_element_by_partial_link_text("Export").click()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        wait_for(self.driver, By.LINK_TEXT, "OK")
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_partial_link_text("OK").click())
            
    def parse_file(self, account, f):
        transactions = []
        f.next()
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.datetime.strptime(row['Date'][0:10], '%m/%d/%Y').date()
            action = row['Action']
            symbol = row['Symbol']
            description = row['Description']
            #quantity = row['Quantity']
            #price = row['Price']
            #fees = row['Fees & Comm']
            amount = row['Amount']
            
            if amount:
                amount = float(amount.replace('$', ''))
                full_description = action
                if symbol:
                    full_description = '{} - {}'.format(action, description)
                transactions.append({'posted':date,
                                    'description':full_description,
                                    'amount':amount})
        return Statement(account, transactions, self._statement.balance)