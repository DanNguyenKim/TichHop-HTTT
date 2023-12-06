from django.urls import path
from . import views
from .views import chat
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup',views.Signup.as_view(),name='signup'),
    path('login',views.Login.as_view(),name='login'),
    path('logout',views.Login.logout,name='logout'),
    path('cart',views.Cart.as_view(),name='cart'),
    path('check-out',views.Checkout.as_view(),name='checkout'),
    path('orders',views.Orders.as_view(),name='orders'),
    # path('detail',views.Detail.as_view(),name='detail'),
    path('detail-order',views.Orders.as_view(),name='detail-order'),
    path('continues',views.Index.as_view(),name='continues'),
    path('comments',views.Comments.as_view(),name='comments'),
    path('delete',views.Cart.as_view(),name='cart'),
    # path('chat',views.Chat.as_view(),name='chat'),
    # path('chat', views.Chats.as_view(), name='query')
    path('chat/', chat, name='chat')
]