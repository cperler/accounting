from django.db import models


class BalanceManager(models.Manager):
    def snap(self, as_of_date, account, balance):
        from accounting.models import Account

        existing_balance = self.filter(as_of_date=as_of_date, account=account)
        if existing_balance.exists():
            print 'Found balance - updating to: ', balance
            existing_balance.update(amount=balance)
        else:        
            balance, _ = self.get_or_create(as_of_date=as_of_date, account=account, amount=balance)
            print 'Created balance: ', balance
        for other_account in Account.objects.all().exclude(id=account.id):
            balance_for_account = self.filter(as_of_date=as_of_date, account=other_account)
            if not balance_for_account.exists():
                prior_balance = 0.0
                if self.filter(account=other_account).exists():
                    prior_balance = self.filter(account=other_account).order_by('-as_of_date')[0].amount
                print 'Updating balance for other account: ', other_account, prior_balance
                self.create(as_of_date=as_of_date, account=other_account, amount=prior_balance)
                
