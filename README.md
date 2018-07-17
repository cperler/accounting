I'm a bit anal about tracking my finances.  Every few days or weeks, I'll go through my accounts - checking, savings, investments, loans, mortgage, etc... and download them all, put them into a spreadsheet, and do analyses.  Is my net worth increasing?  What is my family spending the most money on?  How are things changing month-to-month?  Are there any transactions that I can't identify?

Yes, this takes a long time, and yes, there are tools for managing all of this.  I've tried these tools - Quicken and Mint, for example.  Neither gives me the level of control I want.  It's a pain to categorize transactions and generate reports and graphs, and these tools don't give me the flexibility to do whatever I want with them.  So I stuck it out with Excel.

Well, I'm an engineer, so what the hell man?  I can build a tool that automates this crappy exercise so that I can get to the analysis I really want.  Thus, this project.  Using selenium, django and some html parsing, we can automate downloading transactions and balances, and then organize them whatever way we want.  Some financial firms make it easy to get at this information, others are difficult.  We're better then them though.

This project is not meant for production use.  It's meant for running locally for your own purposes.  There's no encryption around account passwords.  I've only tested the available providers with Chrome, so that needs to be available in the local environment.

The way this works is that you create Accounts.  In order to automatically download and process transactions, an Account requires a username and password, and a reference to a provider, which does the actual work of downloading and processing.  Some providers require a bit more information, such as a download URL or a "site key" which is usually the account name as it's listed on the financial firm's page.  See each provider for more information.

As an example:

```
from accounting.models import *
from accounting.providers.chase import *
a = Account.objects.get(name='Chase-Savings')
c = Chase()
c.retrieve(a)
# wait a bit while Chase donwloads all transactions and the current balance for the Chase-Savings account
# Output: c.retrieve(a)

c.process()
# Output: Found balance - updating to:  xxxx
# Output: Created transaction:  2015-04-08 12:00:00 Chase-Savings INTEREST PAYMENT 0.03 None
# Output: Created transaction:  2015-03-09 12:00:00 Chase-Savings INTEREST PAYMENT 0.03 None
# Output: Created transaction:  2015-02-09 12:00:00 Chase-Savings INTEREST PAYMENT 0.03 None
# ...
```

There's plenty of room for improvement, but that's the point.  Once you have easy access to your consolidated finances, you're empowered to do whatever you want with them.

Feel free to reach out if you have any questions.
