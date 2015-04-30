from django.contrib.auth.models import User
from django.db import models

from accounting.managers import BalanceManager
from accounting.providers.amex import AmEx
from accounting.providers.capitalone import CapitalOne
from accounting.providers.chase import Chase, ChaseMortgage
from accounting.providers.citi import Citibank, Citicard, SearsCard
from accounting.providers.discover import DiscoverStudentLoan
from accounting.providers.nyctrs import NYCTrs
from accounting.providers.penn import PennLifeInsurance
from accounting.providers.schwab import Schwab
from accounting.providers.streetscape import Streetscape
from accounting.providers.transamerica import Transamerica


class AccountOwner(models.Model):
    name        = models.CharField(max_length=150, unique=True)
    user        = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class AccountType(models.Model):
    name    = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.name

ASSETS = 0
LIABILITIES = 1
class Account(models.Model):
    ACCOUNT_DESIGNATION = ((ASSETS, 'Assets'), (LIABILITIES, 'Liabilities'))
    
    CHASE = 0
    CAPITAL_ONE = 1
    CITIBANK = 2
    SCHWAB = 3
    AMEX = 4
    CITICARD = 5
    TRANSAMERICA = 6
    STREETSCAPE = 7
    SEARSCARD = 8
    NYCTRS = 9
    DISCOVER_SL = 10
    CHASE_MTG = 11
    PENN_LIFE = 12
    PROVIDERS = ((CHASE, Chase), (CAPITAL_ONE, CapitalOne), (CITIBANK, Citibank), (SCHWAB, Schwab),
                 (AMEX, AmEx), (CITICARD, Citicard), (TRANSAMERICA, Transamerica),
                 (STREETSCAPE, Streetscape), (SEARSCARD, SearsCard), (NYCTRS, NYCTrs),
                 (DISCOVER_SL, DiscoverStudentLoan), (CHASE_MTG, ChaseMortgage),
                 (PENN_LIFE, PennLifeInsurance))        

    name        = models.CharField(help_text='Will auto-populate if blank upon saving.', 
                                   max_length=150, unique=True, blank=True)
    institute   = models.CharField(max_length=150)
    number      = models.CharField(max_length=50, null=True, blank=True)
    site_key    = models.CharField(max_length=150, null=True, blank=True)
    type        = models.ForeignKey(AccountType, null=True, blank=True)
    provider    = models.IntegerField(choices=PROVIDERS, null=True, blank=True)
    designation = models.IntegerField(choices=ACCOUNT_DESIGNATION, default=ASSETS)
    owner       = models.ForeignKey(AccountOwner, null=True, blank=True)
    login_url   = models.URLField(null=True, blank=True)
    download_url= models.URLField(null=True, blank=True)
    username    = models.CharField(max_length=150, null=True, blank=True)
    password    = models.CharField(max_length=150, null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['last_update', 'name']
    
    def save(self, *args, **kwargs):
        name = self.name
        if name is None or name == '':
            if self.type:
                name = '{}-{}'.format(self.institute, self.type)
                if self.number:
                    name = '{} ({})'.format(name, self.number)
                self.name = name 
        super(Account, self).save(*args, **kwargs)
        
    def get(self):
        if self.provider is not None:
            provider = Account.PROVIDERS[self.provider][1]()
            provider.retrieve(self)
            return provider
        return None
    
    def __unicode__(self):
        return self.name
    
    @property
    def heading(self):
        return self.name

class Category(models.Model):
    name        = models.CharField(max_length=150, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    
    @property
    def heading(self):
        return self.name

class Entity(models.Model):
    description = models.CharField(max_length=150)
    category    = models.ForeignKey(Category)
    
    class Meta:
        verbose_name_plural = 'Entities'

    def __unicode__(self):
        return self.description
    
    @property
    def heading(self):
        return self.description

    
class Alias(models.Model):
    regex       = models.CharField(max_length=300)
    replacement = models.CharField(max_length=150)
    
    class Meta:
        verbose_name_plural = 'Aliases'
        
    def save(self, *args, **kwargs):
        super(Alias, self).save(*args, **kwargs)
        existing_entity = Entity.objects.filter(description=self.replacement)
        matching_entities = Entity.objects.filter(description__icontains=self.regex)
        
        category, _ = Category.objects.get_or_create(name='Unknown')
        if existing_entity.exists():
            category = existing_entity[0].category
        else:
            if matching_entities.exists():
                category = matching_entities[0].category
                
        entity_to_use, _ = Entity.objects.get_or_create(description=self.replacement,
                                                        category=category)
            
        for entity in matching_entities:
            for transaction in entity.transaction_set.all():
                transaction.entity = entity_to_use
                transaction.save()
            if entity != entity_to_use:
                entity.delete()

class Transaction(models.Model):
    posted      = models.DateField(db_index=True)
    account     = models.ForeignKey(Account)
    description = models.CharField(max_length=2000)
    display_txt = models.CharField(max_length=2000)
    entity      = models.ForeignKey(Entity)
    fitid       = models.CharField(max_length=255, null=True, blank=True)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    check_num   = models.PositiveIntegerField(null=True, blank=True)
    notes       = models.TextField(null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted', 'account__name', 'amount']
        
    def save(self, *args, **kwargs):
        if self.display_txt is None or self.display_txt == '':
            self.display_txt = self.description
        super(Transaction, self).save(*args, **kwargs)
    
    @property
    def abs_amount(self):
        return abs(self.amount)
    
    @property
    def is_increase(self):
        if self.account.designation == ASSETS and self.amount > 0:
            return True
        if self.account.designation == LIABILITIES and self.amount < 0:
            return True
        return False
        
    @property
    def is_decrease(self):
        return not self.is_increase()
    
    def __unicode__(self):
        return '{} {} {} {} {}'.format(self.posted, self.account, self.entity, self.amount, self.check_num)
    
    @property
    def heading(self):
        return self.description
    
class Balance(models.Model):
    as_of_date  = models.DateField(db_index=True)
    account     = models.ForeignKey(Account)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    implied     = models.BooleanField(default=False)
    
    unique_together = ('as_of_date', 'account')
    
    objects     = BalanceManager()
    
    class Meta:
        ordering = ['-as_of_date', 'account__designation', 'account__name', 'amount']
    
    @property
    def signed_amount(self):
        if self.account.designation == LIABILITIES and self.amount > 0:
            return -1 * self.amount
        return self.amount
    
    def __unicode__(self):
        return '{} {} {}'.format(self.as_of_date, self.account, self.amount)