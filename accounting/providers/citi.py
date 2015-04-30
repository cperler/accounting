import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from accounting.providers import OfxProvider, wait_for, wait_for_file


# TODO: deal with atm pin crap
class Citibank(OfxProvider):
    def login(self, account):
        super(Citibank, self).login(account)
        wait_for(self.driver, By.LINK_TEXT, "Forgot User ID or Password?")
        
        time.sleep(2)
        try:
            self.driver.find_element_by_id("usernameMasked").click()
            self.driver.find_element_by_id("usernameMasked").send_keys(account.username)
        except:
            self.driver.find_element_by_id("username").click()
            self.driver.find_element_by_id("username").send_keys(account.username)
        
        self.driver.find_element_by_id("pwd").send_keys(account.password)
        self.driver.find_element_by_id("pwd").submit()
            
    def download(self, account):
        wait_for(self.driver, By.LINK_TEXT, "Link an Account")
        script = """$('[key="ExpandAllLabel"]').click()"""
        self.driver.execute_script(script)
        time.sleep(2)
        wait_for(self.driver, By.LINK_TEXT, account.site_key)
        self.driver.find_element_by_partial_link_text(account.site_key).click()
        
        time.sleep(2)
        wait_for(self.driver, By.ID, "filterDropDown-button")
        self.driver.find_element_by_id("filterDropDown-button").click()
        self.driver.find_element_by_id("filterDropDown-menu-option-2").click()
        
        wait_for(self.driver, By.LINK_TEXT, 'Download Transactions')
        self.driver.find_element_by_partial_link_text('Download Transactions').click()
        script = """$('#FormatDropDown').find('option[value="OFX"]').attr('selected', true)"""
        wait_for(self.driver, By.LINK_TEXT, 'Next')
        self.driver.execute_script(script)
        self.driver.find_element_by_id('DownLoadActivity_Next').click()
        wait_for(self.driver, By.LINK_TEXT, 'Download')
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_id('DownLoadActivity_Process').click())
            
class Citicard(OfxProvider):
    def login(self, account):
        super(Citicard, self).login(account)
        
        time.sleep(2)
        self.driver.find_element_by_id("cA-cardsUseridMasked").send_keys(account.username)
        self.driver.find_element_by_name("PASSWORD").send_keys(account.password)
        self.driver.find_element_by_name("PASSWORD").submit()
        
    def download(self, account):
        wait_for(self.driver, By.PARTIAL_LINK_TEXT, account.site_key)
        self.driver.find_element_by_partial_link_text(account.site_key).click()
        
        wait_for(self.driver, By.ID, "filterDropDown-button")
        self.driver.find_element_by_id("filterDropDown-button").click()
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu").send_keys(Keys.PAGE_DOWN)
        self.driver.find_element_by_id("filterDropDown-menu-option-10").click()
        
        wait_for(self.driver, By.LINK_TEXT, 'Download Transactions')
        self.driver.find_element_by_partial_link_text('Download Transactions').click()
        script = """$('#FormatDropDown').find('option[value="OFX"]').attr('selected', true)"""
        wait_for(self.driver, By.LINK_TEXT, 'Next')
        self.driver.execute_script(script)
        self.driver.find_element_by_id('DownLoadActivity_Next').click()
        wait_for(self.driver, By.LINK_TEXT, 'Download')
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_id('DownLoadActivity_Process').click())
        
class SearsCard(Citibank):
    def login(self, account):
        super(Citibank, self).login(account)
        
        self.driver.find_element_by_id("USERNAME-citiTextBlur")
        self.driver.find_element_by_id("USERNAME-citiTextBlur").send_keys(account.username)
        self.driver.find_element_by_id("PASSWORD").send_keys(account.password)
        self.driver.find_element_by_id("PASSWORD").submit()
            
    def download(self, account):
        return wait_for_file(self.dl_path, lambda:self.driver.get("https://www.accountonline.com/cards/svc/OfxStatement.do?dateRange=01/01/2015&viewType=MONEY"))