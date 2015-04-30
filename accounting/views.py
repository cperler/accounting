from _collections import defaultdict
import datetime
from decimal import Decimal

from django.core import cache
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from accounting.models import Transaction, Account, Balance, Entity, Category
from accounting.providers import NoStatementException


months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
first_of_year = datetime.datetime.strptime('01/01/2015', '%m/%d/%Y')

def classify(amount):
    if amount and amount > 0: return 'positive'
    elif amount and amount < 0: return 'negative'
    return 'zero'

class Cell(object):
    def __init__(self, amount, col_change, row_change):
        super(Cell, self).__init__()
        self.amount = amount
        self.col_change = col_change
        self.row_change = row_change

    @property
    def cell_class(self):
        return classify(self.amount)
    
    @property
    def col_class(self):
        return classify(self.col_change)
    
    @property
    def row_class(self):
        return classify(self.row_change)

class Table(object):
    def __init__(self, cols=[], rows=[]):
        super(Table, self).__init__()
        self.cols = cols
        self.rows = rows
        self.cells = defaultdict(lambda : defaultdict(Decimal))
        self.col_totals = defaultdict(Decimal)
        self.row_totals = defaultdict(Decimal)

    def add(self, col, row, amount):
        if col not in self.cols:
            self.cols.append(col)
        if row not in self.rows:
            self.rows.append(row)
        self.cells[col][row] += amount
        self.col_totals[col] += amount
        self.row_totals[row] += amount
    
    def get_cell(self, col, row):
        amount = self.cells[col][row]
        
        col_idx = self.cols.index(col)
        col_diff = None
        if col_idx > 0:
            prior_col = self.cols[col_idx-1]
            prior_cell = self.cells[prior_col][row]
            col_diff = amount-prior_cell        
        return Cell(amount, col_diff, 0)
    
    def get_col_total(self, col):
        amount = self.col_totals[col]
        
        col_idx = self.cols.index(col)
        col_diff = None
        if col_idx > 0:
            prior_col = self.cols[col_idx-1]
            prior_cell = self.col_totals[prior_col]
            col_diff = amount-prior_cell
        return Cell(amount, col_diff, 0)

def _get(request, catfn=lambda tx:tx.entity.category):
    title = 'All Transactions'
    account_id = None
    entity_id = None
    category_id = None
    
    if request.GET:
        account_id = request.GET.get('account_id', None)
        entity_id = request.GET.get('entity_id', None)
        category_id = request.GET.get('category_id', None)
    
    transactions = Transaction.objects.filter(posted__gte=first_of_year)
    if account_id:
        title = 'Account = {}'.format(Account.objects.get(id=account_id).heading)
        transactions = transactions.filter(account__id=account_id)
    if entity_id:
        title = 'Entity = {}'.format(Entity.objects.get(id=entity_id).heading)
        catfn=lambda tx:tx
        transactions = transactions.filter(entity__id=entity_id)
    if category_id:
        title = 'Category = {}'.format(Category.objects.get(id=category_id).heading)
        catfn=lambda tx:tx.entity
        transactions = transactions.filter(entity__category__id=category_id)
    
    total_table = Table(cols=months)
    
    for tx in transactions:
        month = tx.posted.strftime('%b').upper()
        amount = tx.amount
        category = catfn(tx)
        total_table.add(month, category, amount)

    accounts = Account.objects.all()
    balances = Balance.objects.all()
    total = sum([t.amount for t in transactions])
    
    balance_dates = set([b.as_of_date for b in balances])
    balance_amounts = defaultdict(lambda : defaultdict(Decimal))
    balance_totals = defaultdict(Decimal)
    for balance in balances:
        date = balance.as_of_date
        amount = balance.signed_amount
        account = balance.account
        balance_dates.add(date)
        balance_amounts[date][account] += amount
        balance_totals[date] += amount
    balance_dates = sorted(list(balance_dates))
    
    return render_to_response('index.html', {'title':title,
                                             'transactions':transactions,
                                             'accounts':accounts,
                                             'balances':balances,
                                             'totals':total_table,
                                             'balance_dates' : balance_dates,
                                             'balance_amounts' : balance_amounts,
                                             'balance_totals' : balance_totals,
                                             'total':total}, RequestContext(request))

def index(request):
    return _get(request)

def update(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        provider = account.get()
        if provider:
            provider.process()
            account.last_update = datetime.datetime.now()
            account.save()
    except NoStatementException as nse:
        print 'Updating account with error {}: {}'.format(account, nse) 
        account.last_update = datetime.datetime.now()
        account.save()
    except Exception as e:
        print 'Unable to update account {}: {}'.format(account, e)
    return HttpResponseRedirect('/')

def refresh_all(request):
    for account in Account.objects.filter(last_update__lt=datetime.date.today()):
        print 'Refreshing {}.'.format(account)
        try:
            provider = account.get()
            if provider:
                provider.process()
                account.last_update = datetime.datetime.now()
                account.save()
        except NoStatementException as nse:
            print 'Updating account with error {}: {}'.format(account, nse) 
            account.last_update = datetime.datetime.now()
            account.save()
        except Exception as e:
            print 'Unable to update account {}: {}'.format(account, e)
    return HttpResponseRedirect('/')
