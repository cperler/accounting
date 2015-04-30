from selenium.webdriver.common.by import By

from accounting.providers import OfxProvider, wait_for, wait_for_file


class CapitalOne(OfxProvider):
    def login(self, account):
        super(CapitalOne, self).login(account)
        self.driver.switch_to.frame(self.driver.find_element_by_id("loginframe"))
        self.driver.find_element_by_id("uname").send_keys(account.username)
        self.driver.find_element_by_name("password").send_keys(account.password)
        self.driver.find_element_by_name("password").submit()

    def download(self, account):
        wait_for(self.driver, By.LINK_TEXT, "Payment Activity")        
        self.driver.get('https://services2.capitalone.com/accounts/transactions/export')
        
        wait_for(self.driver, By.LINK_TEXT, "Pending transactions")
        return wait_for_file(self.dl_path, lambda:self.driver.get(account.download_url))