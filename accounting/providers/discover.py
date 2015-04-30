from lxml import etree

from accounting.providers import XPathProvider, Statement


class DiscoverStudentLoan(XPathProvider):
    def login(self, account):
        super(DiscoverStudentLoan, self).login(account)
        self.driver.find_element_by_id("ctl00_ctl00_ctl00_siteBodyPlaceHolder_uB_b_usernameTextBox").send_keys(account.username)
        self.driver.find_element_by_id("ctl00_ctl00_ctl00_siteBodyPlaceHolder_uB_b_passwordTextBox").send_keys(account.password)
        self.driver.find_element_by_id("ctl00_ctl00_ctl00_siteBodyPlaceHolder_uB_b_continueButton").click()

    def download(self, account):
        parser = etree.HTMLParser(encoding='utf-8')
        doc = etree.fromstring(self.driver.page_source, parser)
        amounts = doc.xpath("//tr/td[3][contains(text(), '$')]/text()")
        total = 0.0
        for amount in amounts:
            f_amount = float(unicode(amount).encode('ascii', 'ignore').replace("$", '').replace(',',''))
            total += f_amount
        return Statement(account, [], total)