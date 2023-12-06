from django.contrib import admin

# Register your models here.

from.models import Product
class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','size','discount','quantity','quantity_sale','quantity_import','date']
    # list_editable = ('discount', )
    list_filter = ("category",)
    readonly_fields=['date','time']
    search_fields = ("price",'name',)
admin.site.register(Product,AdminProduct)

from.models import Category
class AdminCategory(admin.ModelAdmin):
    list_display=['name']

admin.site.register(Category,AdminCategory)

from.models import Customer
class AdinCustomer(admin.ModelAdmin):
    list_display=['first_name','last_name','phone','email','date_register']
    readonly_fields=['first_name','last_name','phone','email','password','date_register','time_register']
admin.site.register(Customer,AdinCustomer)

from.models import Order
class AdinCustomer(admin.ModelAdmin):
    list_display=['product','customer','quantity','price','size','date','method_pay','status'] 
    list_per_page = 5
    list_filter = ("customer",'status','date')
    readonly_fields=['product','customer','quantity','price','size','date','time','address','phone','method_pay']
admin.site.register(Order,AdinCustomer)

admin.site.site_header = "KimDanShop Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Trang quản trị KimDanShop"

from.models import Comment
class AdminComment(admin.ModelAdmin):
    list_display=['customer','product','product_quality','service_qualitty','transport_quanlity','satisfaction_level']
    readonly_fields=['customer','product','product_quality','service_qualitty','transport_quanlity','satisfaction_level',
                    'date_cmt','time_cmt','commets_other']
admin.site.register(Comment,AdminComment)

from.models import Message
class AdminComment(admin.ModelAdmin):
    list_display=['content','timestamp','response','customer']
    readonly_fields=['content','timestamp','response','customer']
admin.site.register(Message,AdminComment)