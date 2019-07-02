"""mysiteS19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.urls import include

#all urls are defined over here
app_name = 'myapp'
urlpatterns = [path(r'index/', views.index, name='index'),
                path(r'about/', views.about, name='about'),
                path(r'<cat_no>',views.detail,name='detail'),
                path(r'products/',views.products,name='products'),
                path(r'place_order/', views.place_order,name='place_order'),
                path(r'products/<prod_id>', views.productdetail,name='productdetail'),
                path(r'login/',views.user_login,name='user_login'),
                path(r'logout/',views.user_logout,name='user_logout'),
                path(r'myorders/',views.myorders,name='my_order'),
                path(r'signup/', views.signup, name="signup"),
                # path(r'password_reset_confirm/<uidb64>/<token>/',
                #    auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),                
                #path(r'password_reset/', auth_views.PasswordResetView.as_view(template_name='myapp/registration/password_reset_form.html'), name='password_reset'),
                #path(r'password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/registration/password_reset_done.html'), name='password_reset_done'),
                
                #path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete')
             ]