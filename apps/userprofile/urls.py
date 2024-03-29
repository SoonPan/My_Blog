from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),

    path('delete/<int:id>/', views.user_delete, name='delete'),

    path('edit/<int:id>/', views.profile_edit, name='edit'),

    path('verify/', views.user_verify, name='verify'),

    path('signup/', views.signup_verify, name='signup'),

]