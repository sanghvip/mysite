from django.contrib import admin
from django.db.models import F
from .models import Product, Category, Client, Order


#ModelAdmin for Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','city','interested_category']
    #method to display list of interested categories
    def interested_category(self,obj):
            #get the value of interested_in field
            interestedCategories = getattr(obj,'interested_in').all()
            #list to hold categories
            categories = []
            for categoryName in interestedCategories:
                categories.append(categoryName)
            
            return categories
    interested_category.short_description = 'Interested category'    
admin.site.register(Client,ClientAdmin)

#action for ProductAdmin to incrementStock of selected product by 50
def incrementStock(modeladmin, request, queryset):
    queryset.update(stock = F('stock')+50)
incrementStock.short_description = "Increase stocks by 50"    


#ModelAdmin for Product
class ProductInline(admin.StackedInline):
    model = Product
    
class ProductAdmin(admin.ModelAdmin):
    #list to display the fields of product model
    list_display = ['name','category','price','available','stock']
    actions = [incrementStock]

#registration of ProductAdmin and Product model    
admin.site.register(Product, ProductAdmin)


#ModelAdmin for Register
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_product_name','get_client_name','num_units','order_status','status_date'] 
    def get_product_name(self,obj):
        return '{}'.format(obj.product.name)
    get_product_name.short_description = 'Product'
    
    def get_client_name(self,obj):
        return '{} {}'.format(obj.client.first_name,obj.client.last_name)
    get_client_name.short_description='Client '
admin.site.register(Order, OrderAdmin)

#ModelAdmin for category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','warehouse'] 
    inlines=[ProductInline]
admin.site.register(Category, CategoryAdmin) 
