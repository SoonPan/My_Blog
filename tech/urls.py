# 引入path
from django.urls import path
from tech import views

# 正在部署的应用的名称
app_name = 'tech'

urlpatterns = [
    # path函数将url映射到视图
    path('', views.tech),

]