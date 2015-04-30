import csv
import datetime
import time

from lxml import etree
from selenium.webdriver.support.ui import Select

from accounting.providers import CSVProvider, Statement, wait_for_file


class Transamerica(CSVProvider):
    def login(self, account):
        super(Transamerica, self).login(account)
        self.driver.find_element_by_id('username').send_keys(account.username)
        self.driver.find_element_by_id('password').send_keys(account.password)
        self.driver.find_element_by_id('password').submit()
            
    def download(self, account):
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        balance = doc.xpath('//*[contains(text(), "Total Balance")]/following-sibling::p/text()')
        balance = float(balance[0].strip().replace('$', '').replace(',', ''))
        self._statement = Statement(account, [], balance)
        
        self.driver.get('https://ddol.divinvest.com/ddol/authenticated/reports/transactionHistory.html')
        time.sleep(2)
        select = Select(self.driver.find_element_by_id('startDate_Month_ID'))
        select.select_by_index(0)
        self.driver.find_element_by_xpath("//a[contains(@href, 'submitted')]").click()

        time.sleep(2)
        self.driver.find_element_by_partial_link_text('download').click()
        script = """$('[name="downloadFormat"]').find('option[value="csv"]').attr('selected', true)"""
        self.driver.execute_script(script)
     
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_name('downloadFormat').submit())
            
    def parse_file(self, account, f):
        transactions = []
        reader = csv.DictReader(f)
        for row in reader:
            transaction_type = row['Transaction Type']
            date = datetime.datetime.strptime(row['Date'], '%m/%d/%y').date()
            source = row['Source'].strip()
            fund = row['Fund Name']
            #unit_count = row['Unit Count']
            #unit_value = row['Unit Value']
            amount = row['Transaction Amount']
            
            if amount:
                amount = float(amount)
                full_description = '{} - {} of {}'.format(transaction_type, source, fund)
                transactions.append({'posted':date,
                                    'description':full_description,
                                    'amount':amount})
        return Statement(account, transactions, self._statement.balance)