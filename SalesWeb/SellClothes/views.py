from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
import re,datetime
import math 
from django.views import View
from.models import Product
from.models import Category
from.models import Customer
from.models import Order
from.models import Comment
from django import template
from django.core.paginator import Paginator

class Index(View):
    def post(self, request):
        product=request.POST.get('product')
        cart=request.session.get('cart')
        remove=request.POST.get('remove')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:            
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        # print(len(request.session['cart']))
        return redirect("index")
    def get(self, request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        product=None
        categories=Category.get_all_categories()
        categoryID=request.GET.get('category')
        size=request.GET.get('size')
        comment_id=request.GET.get('comment_id')
        price_size=request.GET.get('price')
        # print(size)
        # print(request.GET.get('detail'))
        id_detail=request.GET.get('detail')
        if id_detail:
            return render(request,'detail.html',{'products':Product.get_product_by_id(id_detail)})
        elif comment_id:
            product_cmt=Product.get_product_by_id(comment_id)
            return render(request,'comments.html',{'products':product_cmt})
        elif price_size:
            product_pricesize=Product.get_all_products_by_pricesize(price_size)
            return render(request,'index.html',{'products':product_pricesize,'categories':categories})
        else:
            if categoryID:
                product=Product.get_all_products_by_categoryid(categoryID);
            elif size:
                search=size.split('/')
                # print(search)
                product=Product.get_all_products_by_size(int(search[1]),search[0])
            # else:
            #     product=Product.get_all_products();
            # data={}
            # data['products']=product
            # data['categories']=categories
            
            # print(product)
            # return render(request,'index.html',data)
            else:
                product=Product.get_all_products();
            paginator = Paginator(product, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            data={}
            # data['products']=product
            data['products']=page_obj
            data['categories']=categories

            return render(request,'index.html',data)

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        postData=request.POST
        first_name=postData.get('firstname')
        last_name=postData.get('lastname')
        phone=postData.get('phone')
        email=postData.get('email')
        password=postData.get('password')
        # validation
        value={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email,
        }
        error_message=None;
        customer=Customer(first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        password=password)
        #save
        error_message=self.validateCustomer(customer)
        if not error_message:
            customer.password=make_password(customer.password)
            customer.register()
            return redirect('index')
        else:
            data={
                'error':error_message,
                'values':value
            }
            return render(request,'signup.html',data)
    def validateCustomer(self,customer):
        error_message=None
        if not customer.first_name:
            error_message='Bạn chưa nhập tên'
        elif not re.search(r'^\w+$',customer.first_name):
            error_message="Tên không được chứa ký tự đặc biệt hoặc có dấu"
        elif len(customer.first_name)>6:
            error_message="Tên quá dài không hợp lệ"
        elif not customer.last_name:
            error_message='Bạn chưa nhập họ & tên đệm'
        elif not re.search(r'^\w+$',customer.last_name):
            error_message="Họ và tên đệm không được chứa ký tự đặc biệt hoặc có dấu"
        elif len(customer.last_name)<3:
            error_message='Họ và tên đệm quá ngắn'
        elif not customer.phone:
            error_message="Bạn chưa nhập số điện thoại"
        elif len(customer.phone)!=10:
            error_message='Số điện thoại phải có 10 chữ số'
        elif not customer.email:
            error_message='Bạn chưa nhập email'
        elif len(customer.email)<10:
            error_message='Email quá ngắn không hợp lệ'
        elif customer.isExist():
            error_message='Email đã được đăng ký'
        elif not customer.password:
            error_message="Bạn chưa nhập mật khẩu"
        elif len(customer.password)<6:
            error_message='Mật khẩu phải có độ dài lơn hơn 6'
        return error_message

class Login(View):
    def get(self,request):
        return render(request,'login.html')        
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
        error_message=None
        if customer:
            check=check_password(password,customer.password)
            if check:
                request.session['customer']=customer.id
                request.session['email']=customer.email
                return redirect('index')
            else:
                error_message="Email hoặc mật khẩu không hợp lệ!"
        else:
            error_message="Email hoặc mật khẩu không hợp lệ!"
        return render(request,'login.html',{'error':error_message})
    def logout(request):
        # request.session.clear()
        request.session['customer']=False
        return redirect('login')

class Cart(View):
    def post(self,request):
        product=request.POST.get('product')
        cart=request.session.get('cart')
        remove=request.POST.get('remove')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    cart.pop(product)
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        print(len(request.session['cart']))
        ids=list(request.session.get('cart').keys())
        products=Product.get_product_by_id(ids)
        print(products)
        return render(request,'cart.html',{"products":products})
    def get(self,request):
        ids=list(request.session.get('cart').keys())
        products=Product.get_product_by_id(ids)
        print(products)
        return render(request,'cart.html',{"products":products})

class Checkout(View):
    def post(self, request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        method_pay=request.POST.get('method_pay')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.get_product_by_id(list(cart.keys()))
        S=0
        for  product in products:
            order=Order( customer=Customer(id=customer),
                         product=product,   
                         price=math.floor(int(product.price - ( product.price * product.discount * 0.01 )))*int(cart.get(str(product.id))),
                         size=product.size,
                         address=address,
                         phone=phone,
                         quantity=cart.get(str(product.id)),
                         method_pay=method_pay
                        )
            product_update=Product.objects.get(id=product.id)
            product_update.quantity=product_update.quantity - cart.get(str(product.id))
            product_update.quantity_sale=product_update.quantity_sale + cart.get(str(product.id))
            product_update.date=datetime.datetime.today()
            product_update.save()
            order.PlaceOrder()
            S=S+math.floor(int(product.price - ( product.price * product.discount * 0.01 )))*int(cart.get(str(product.id)))
        S=S/23500
        request.session['cart']={}
        if re.search("online",method_pay):
            return render(request,'payment_online.html',{'products':round(S,2)})

        else:
            return render(request,'thanks.html')

class Orders(View):
    def get(self, request):
        customer=request.session.get('customer')
        orders=Order.get_orders_by_customer(customer)
        return render(request,'orders.html',{'orders':orders})

# class Detail(View):
#     def get(self, request):
#         comment_id=request.GET.get('comment_id')
#         print(comment_id)
#         if comment_id :
#             return render(request,'comments.html')
#         return render(request,'detail.html')

class Comments(View):
    def get(self, request):
        return render(request,'comments.html')
    def post(self, request):
        product_id=request.POST.get('product')
        products=Product.get_product_by_id(ids=product_id)
        customer=request.session.get('customer')
        product_quality=request.POST.get('product_quality')
        service_qualitty=request.POST.get('service_qualitty')
        transport_quanlity=request.POST.get('transport_quanlity')
        satisfaction_level=request.POST.get('satisfaction_level')
        commets_other=request.POST.get('cmt')
        print(product_id,customer,product_quality,service_qualitty,transport_quanlity,satisfaction_level,commets_other)
        for product in products:
            comments=Comment(customer=Customer(id=customer),
                            product=product,
                            product_quality=product_quality,
                            service_qualitty=service_qualitty,
                            transport_quanlity=transport_quanlity,
                            satisfaction_level=satisfaction_level,
                            commets_other=commets_other,
                        )
            comments.save()
        return redirect('index')

# class Chats(View):
#     def get(self, request):
#         return render(request,'chat.html')
#     def post(self,request):
#         return redirect('chat.html')


# from django.shortcuts import render
# from django.http import JsonResponse
# # import openai
  
# # openai.api_key = 'YOUR_API_KEY'
  
# def get_completion(prompt):
#     print(prompt)
#     # query = openai.Completion.create(
#     #     engine="text-davinci-003",
#     #     prompt=prompt,
#     #     max_tokens=1024,
#     #     n=1,
#     #     stop=None,
#     #     temperature=0.5,
#     # )
  
#     # response = query.choices[0].text
#     response=" Hello"
#     print(response)
#     return response
#     # pass
  
  
# def query_view(request):
#     if request.method == 'POST':
#         prompt = request.POST.get('prompt')
#         response =get_completion(prompt)
#         return JsonResponse({'response': response})
#     return render(request,'chat.html')

# views.py
from django.shortcuts import render, redirect
from .models import Message
import requests
import base64
from django.contrib import messages
from io import BytesIO
def response_user(content):
    # Địa chỉ URL của API bạn muốn gọi
    # # llama
    # api_url = "https://4add-34-116-89-113.ngrok-free.app/chatbot" 

    # # falcon
    api_url = "https://3b1c-35-223-102-205.ngrok-free.app/chatbot" 

    # Dữ liệu bạn muốn gửi dưới dạng JSON
    data = {
        "prompt": str(content)
    }

    # Gửi yêu cầu POST đến API với dữ liệu JSON
    response = requests.post(api_url, json=data)

    # Kiểm tra xem yêu cầu có thành công không (status code 200)
    if response.status_code == 200:
        # Lấy nội dung của phản hồi dưới dạng văn bản
        api_data = response.text
        decoded_bytes = base64.b64decode(api_data)
        decoded_text = decoded_bytes.decode("utf-8")
        # print(decoded_text)
        return decoded_text
    else:
        # print(f"Lỗi trong việc gọi API. Status code: {response.status_code}")
        return f"Lỗi trong việc gọi API. Status code: {response.status_code}"
def chat(request):
    # messages = Message.objects.all()

    # if request.method == 'POST':
    #     content = request.POST.get('content')
    #     if content:
    #         response = response_user(content)  # Hàm này để lấy phản hồi từ bên thứ ba
    #         Message.objects.create(content=content, response=response)
    #         return redirect('chat')

    # return render(request, 'chat.html', {'messages': messages})
    customer=request.session.get('customer')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            response = response_user(content)  # Hàm này để lấy phản hồi từ bên thứ ba
            Message.objects.create(customer=Customer(id=customer), content=content, response=response,timestamp=datetime.datetime.today())
            messages.success(request, 'Message sent successfully!')

            return redirect('chat')

    messages_list = Message.objects.filter(customer=customer)

    return render(request, 'chat.html', {'messages': messages_list})
    

