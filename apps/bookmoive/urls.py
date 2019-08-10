# 引入path
from django.urls import path
from apps.bookmoive import views

# 正在部署的应用的名称
app_name = 'bookmoive'

urlpatterns = [
    # path函数将url映射到视图
    path('', views.bookmoive),

]