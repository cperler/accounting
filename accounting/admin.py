from django.contrib import admin

from accounting.models import AccountOwner, AccountType, Account, Category, \
    Entity, Transaction, Alias, Balance


class AccountOwnerAdmin(admin.ModelAdmin):
    list_display        = ('name', 'user')
admin.site.register(AccountOwner, AccountOwnerAdmin)

class AccountTypeAdmin(admin.ModelAdmin):
    list_display        = ('name', )
admin.site.register(AccountType, AccountTypeAdmin)

def connected(instance):
    return instance.provider is not None
connected.boolean = True

class AccountAdmin(admin.ModelAdmin):
    list_display        = ('name', 'type', 'designation', 'institute', 'login_url', connected)
    
    def get_ordering(self, request):
        return ['designation', 'type', 'name']
admin.site.register(Account, AccountAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name',)
admin.site.register(Category, CategoryAdmin)

class EntityAdmin(admin.ModelAdmin):
    list_display        = ('description', 'category')
    
    def get_ordering(self, request):
        return ['description', 'category']
admin.site.register(Entity, EntityAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display        = ('posted', 'account', 'entity', 'amount', 'check_num')
    
    def get_ordering(self, request):
        return ['posted', 'entity', 'amount']
admin.site.register(Transaction, TransactionAdmin)

class AliasAdmin(admin.ModelAdmin):
    list_display        = ('regex', 'replacement')
admin.site.register(Alias, AliasAdmin)

class BalanceAdmin(admin.ModelAdmin):
    list_display        = ('as_of_date', 'account', 'amount')
admin.site.register(Balance, BalanceAdmin)