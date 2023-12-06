from django.db import models
from django.utils import timezone
# Create your models here.

import datetime
class Customer(models.Model):
    first_name = models.CharField('Tên',max_length=50)
    last_name = models.CharField('Họ & tên đệm',max_length=50)
    phone = models.CharField('Số điện thoại',max_length=15)
    email = models.EmailField()
    password = models.CharField('Mật khẩu',max_length=500)
    date_register=models.DateField('Ngày đăng ký',default=datetime.datetime.today)
    time_register=models.TimeField('Thời gian đăng ký',default=datetime.datetime.today)
    class Meta:
        verbose_name_plural = "Khách hàng đăng ký"
    def __str__(self):
        return 'Khách hàng '+ self.first_name

    def register(self):
        self.save()
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

class Category(models.Model):
    name = models.CharField('Loại sản phẩm',max_length=20)
    class Meta:
        verbose_name_plural = "Loại sản phẩm"
    def __str__(self):
        return self.name
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
class Pricesize(models.Model):
    name=models.CharField('Khoảng giá sản phẩm',max_length=30)
    class Meta:
        verbose_name_plural = "Khoảng giá sản phẩm"
    def __str__(self):
        return self.name
    @staticmethod
    def get_all_pricesize():
        return Pricesize.objects.all()

class Product(models.Model):
    name = models.CharField('Tên sản phẩm',max_length=50)
    price = models.IntegerField('Giá sản phẩm',default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,verbose_name='Loại sản phẩm')
    price_size=models.ForeignKey(Pricesize,on_delete=models.CASCADE, default=1,verbose_name='Khoảng giá')
    description = models.CharField('Mô tả',max_length=200, default='' , null=True , blank=True)
    image = models.ImageField('Ảnh',upload_to='static/images/')
    quantity=models.IntegerField('Số lượng hàng còn',default=200)
    quantity_sale=models.IntegerField('Số lượng đã bán',default=0)
    quantity_import=models.IntegerField('Số lượng mới nhập',default=0)
    discount=models.IntegerField('Giảm giá',null=False , default = 0)
    size_choices=[('S','S'),('M','M'),('L','L')]
    size=models.CharField('Size',choices=size_choices,max_length=10,default='M' , null=True , blank=True)
    date=models.DateField("Ngày đặt cuối",)
    time=models.TimeField('Thời gian đặt cuối',)
    class Meta:
        verbose_name_plural = "Sản phẩm"
    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products();
    @staticmethod
    def get_all_products_by_size(category,size):
        return Product.objects.filter(category=category,size=size)
    @staticmethod
    def get_all_products_by_pricesize(price_size):
        return Product.objects.filter(price_size=price_size)
            

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Tên sản phẩm',)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Tên Khách hàng')
    size=models.CharField('Size',max_length=10,default='', null=True , blank=True)
    quantity=models.IntegerField('Số lượng đặt',default=1)
    price=models.IntegerField('Giá thanh toán')
    address=models.CharField('Địa chỉ',max_length=50, default='',blank=True)
    phone=models.CharField('Số điện thoại',max_length=10,default='',blank=True)
    date=models.DateField('Ngày đặt',default=datetime.datetime.today)
    time=models.TimeField('Thời gian đặt',default=datetime.datetime.today)
    method_pay=models.CharField('Phương thức thanh toán',max_length=30,default='Thanh toán khi nhận hàng', blank=True)
    status=models.BooleanField('Xác nhận đơn',default=False)
    
    class Meta:
        verbose_name_plural = "Đơn hàng"
    def PlaceOrder(self):
        self.save()
    def __str__(self):
        return "Đơn hàng của "+self.customer.first_name
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
class Comment(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Khách hàng phản hồi')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Sản phẩm phản hồi')
    product_quality=models.CharField('Chất lượng sản phẩm',max_length=100,default='',blank=True)
    service_qualitty=models.CharField('Chất lượng dịch vụ',max_length=100,default='',blank=True)
    transport_quanlity=models.CharField('Chất lượng vận chuyển',max_length=100,default='',blank=True)
    satisfaction_level=models.CharField('Mức độ hài lòng',max_length=100,default='',blank=True)
    commets_other=models.TextField('Ý kiến khác',max_length=100,default='',blank=True)
    date_cmt=models.DateField('Ngày phản hồi',default=datetime.datetime.today)
    time_cmt=models.TimeField('Thời gian phản hồi',default=datetime.datetime.today)
    class Meta:
        verbose_name_plural = "Phản hồi khách hàng"
    
    def __str__(self):
        return "Phản hồi của khách hàng "+ "\"" +self.customer.first_name+ "\""
    
from django.db import models
from django.utils import timezone

class Message(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, default="1")
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.today)
    response = models.TextField(blank=True, null=True)