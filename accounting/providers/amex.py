import time

from accounting.providers import OfxProvider, wait_for_file


class AmEx(OfxProvider):
    def login(self, account):
        super(AmEx, self).login(account)
        self.driver.find_element_by_id("lilo_userName").send_keys(account.username)
        self.driver.find_element_by_id("lilo_password").send_keys(account.password)
        self.driver.find_element_by_id("lilo_password").submit()
            
    def download(self, account):
        self.driver.get(account.download_url)
        self.driver.execute_script("$('span.icon-checkbox').click()")
        time.sleep(2)
        return wait_for_file(self.dl_path, lambda:self.driver.find_element_by_xpath("//button[@id='downloadFormButton']").click())