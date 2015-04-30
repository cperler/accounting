import csv
import datetime

from selenium.webdriver.common.by import By

from accounting.providers import CSVProvider, wait_for, wait_for_file, Statement
from lxml import etree


class Streetscape(CSVProvider):
    def login(self, account):
        super(Streetscape, self).login(account)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        self.driver.find_element_by_name("UserID").send_keys(account.username)
        self.driver.find_element_by_name("UserPwd").send_keys(account.password)
        self.driver.find_element_by_id("loginbutton").click()
        
    def download(self, account):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(1)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        balance = doc.xpath('//*[contains(text(), "Portfolio Total")]/text()')
        balance = float(balance[0].strip().replace('Portfolio Total: $', '').replace(',',''))
        self._statement = Statement(account, [], balance)

        self.driver.find_element_by_partial_link_text(account.site_key).click()
        self.driver.switch_to.frame(0)
        self.driver.find_element_by_id("pageTitledwnArr").click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(9)
        self.driver.find_element_by_partial_link_text("Your Default").click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(1)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(1)
        wait_for(self.driver, By.PARTIAL_LINK_TEXT, 'Important History Information')
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_id("export").click())
            
    def parse_file(self, account, f):
        f.next()
        f.next()
        f.next()
        f.next()
        transactions = []
        reader = csv.DictReader(f)
        for row in reader:
            if row['Entry Date']:
                date = datetime.datetime.strptime(row['Entry Date'], '%d-%b-%Y')
                #transaction_type = row['Transaction Type']
                description = row['Transaction Description']
                symbol = row['Security ID']
                #symbol_description = row['Security Description']
                #quantity = row['Quantity']
                #price = row['Price']
                #fees = row['Fees & Comm']
                amount = row['Net Amount']
                
                if amount:
                    amount = float(amount.replace('$', ''))
                    full_description = description
                    if symbol and symbol != '--':
                        full_description = '{} - {}'.format(description, symbol)
                    transactions.append({'posted':date,
                                        'description':full_description,
                                        'amount':amount})
        return Statement(account, transactions, self._statement.balance)