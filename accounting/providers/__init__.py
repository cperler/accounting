import datetime
import os
import time

from ofxparse.ofxparse import OfxParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def file_count(path):
    return len([name for name in os.listdir(path) if os.path.isfile(path+'/'+name)])

def newest_file(path):
    dated_files = [(os.path.getmtime(path+'/'+fn), os.path.basename(path+'/'+fn)) for fn in os.listdir(path)]
    dated_files.sort()
    dated_files.reverse()
    return dated_files[0][1]
    
def wait_for_file(path, get_file_fn):
    start_file_count = file_count(path)
    end_file_count = start_file_count
    
    get_file_fn()
    
    while start_file_count == end_file_count:
        end_file_count = file_count(path)
        time.sleep(1)
    
    newest = None
    while newest is None or 'crdownload' in newest:
        newest = newest_file(path)
        time.sleep(1)
    
    print 'Found file! ', newest
    return newest
    
def wait_for(driver, by, value):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

class Statement(object):
    def __init__(self, account, transactions=None, balance=None):
        self.account = account
        self.transactions = transactions
        self.balance = balance
    
class NoStatementException(Exception):
    pass
    
class FinancialProvider(object):
    def __init__(self):
        self.dl_path = '/users/craigperler/Downloads/'
        self._statement = None
        
    @property
    def transaction(self):
        return self._statement.transactions if self._statement else []
        
    @property
    def balance(self):
        return self._statement.balance if self._statement else None
        
    def login(self, account):
        self.driver = webdriver.Chrome()
        self.driver.get(account.login_url)
    
    def download(self, account):
        raise Exception('Not implemented.')
    
    def _download(self, account):
        try:
            return self.download(account)
        except Exception as e:
            print e
        finally:
            self.driver.quit()

    def parse(self, account, file_or_statement):
        if self._statement is not None:
            raise Exception('Already parsed file or statement.')
        
        if file_or_statement is None:
            raise NoStatementException('No file or statement is available following download.')
            
    def retrieve(self, account):
        if self._statement is None:
            self.login(account)
            file_or_statement = self._download(account)
            self.parse(account, file_or_statement)
                                
    def process(self):
        if self._statement is None or self._statement.account is None:
            return

class XPathProvider(FinancialProvider):
    def parse(self, account, statement):
        super(XPathProvider, self).parse(account, statement)
        self._statement = statement
                
    def process(self):
        super(XPathProvider, self).process()
        
        from accounting.models import Category, Entity, Transaction, Alias, Balance
        
        unknown_category, _ = Category.objects.get_or_create(name='Unknown')
        
        Balance.objects.snap(datetime.date.today(), self._statement.account, self._statement.balance)
        
        for row in self._statement.transactions:
            posted = row['posted']
            description = row['description']
            
            for alias in Alias.objects.all():
                if alias.regex.lower() in description.lower():
                    description = alias.replacement
                    break
            
            if Entity.objects.filter(description=description).exists():
                entity = Entity.objects.get(description=description)
            else:
                entity, _ = Entity.objects.get_or_create(description=description,
                                                         category=unknown_category)
            amount = float(row['amount'])
                
            if not Transaction.objects.filter(posted=posted,
                                          description=description, 
                                          account=self._statement.account, 
                                          amount=amount).exists():
                tnx, _ = Transaction.objects.get_or_create(posted=posted,
                                                            description=description, 
                                                            account=self._statement.account, 
                                                            entity=entity,
                                                            amount=amount)
            
                print 'Created transaction: ', tnx


class CSVProvider(XPathProvider):
    def parse(self, account, _file, keep_file=True):
        full_path = self.dl_path + '/' + _file

        try:
            with open(full_path) as f:
                self._statement = self.parse_file(account, f)
        except Exception as e:
            print e
        finally:
            if not keep_file:
                os.remove(full_path)
                
class OfxProvider(FinancialProvider):
    def parse(self, account, _file, keep_file=False):
        super(OfxProvider, self).parse(account, _file)
        full_path = self.dl_path + '/' + _file

        try:
            with open(full_path) as f:
                self._statement = self.parse_file(account, f)
        except Exception as e:
            print e
        finally:
            if not keep_file:
                os.remove(full_path)
                
    def parse_file(self, _account, f):
        parsed_file = OfxParser.parse(f)
        transactions = []
        for account in parsed_file.accounts:
            transactions.extend(account.statement.transactions)
        try:
            balance = parsed_file.account.statement.balance
        except:
            balance = parsed_file.account.statement.available_balance
        return Statement(_account, transactions, balance)
                                
    def process(self):
        super(OfxProvider, self).process()
        
        from accounting.models import Category, Entity, Transaction, Alias, Balance

        unknown_category, _ = Category.objects.get_or_create(name='Unknown')
        
        Balance.objects.snap(datetime.date.today(), self._statement.account, self._statement.balance)
        
        for row in self._statement.transactions:
            fitid = row.id
            memo = row.memo
            posted = row.date
            description = row.payee
            
            for alias in Alias.objects.all():
                if alias.regex.lower() in description.lower():
                    description = alias.replacement
                    break
            
            if Entity.objects.filter(description=description).exists():
                entity = Entity.objects.get(description=description)
            else:
                entity, _ = Entity.objects.get_or_create(description=description,
                                                         category=unknown_category)
            amount = float(row.amount)
            check_num = row.checknum
            if len(check_num) > 0:
                if 'CHECK' in check_num:
                    check_num = int(check_num.split(' ')[1])
                else:
                    check_num = int(check_num)
            else:
                check_num = None

            if not Transaction.objects.filter(fitid=fitid,
                                            posted=posted,
                                            description=row.payee, 
                                            account=self._statement.account, 
                                            amount=amount, 
                                            notes=memo,
                                            check_num=check_num).exists():

                tnx, _ = Transaction.objects.get_or_create(fitid=fitid,
                                                            posted=posted,
                                                            description=row.payee, 
                                                            account=self._statement.account, 
                                                            entity=entity,
                                                            amount=amount, 
                                                            notes=memo,
                                                            check_num=check_num)
            
                print 'Created transaction: ', tnx