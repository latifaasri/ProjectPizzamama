from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.registerpage, name="register"),
    path('user/', views.userpage, name="pageuser"),
    path('account/', views.accountSettings, name="account"),

    path('product/', views.products, name="product"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('', views.home, name="Home"),

    path('createorder/<str:pk>', views.createorder, name="createorder"),
    path('updateorder/<str:pk>', views.updateorder, name="updateorder"),
    path('deleteorder/<str:pk>', views.deleteorder, name="deleteorder"),

    #Submit email form       
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    #Email sent success message
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    #Link to password Rest form in email 
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    #Password successfully changed message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
]

