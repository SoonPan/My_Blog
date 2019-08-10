# 引入path
from django.urls import path
from apps.about import views

# 正在部署的应用的名称
app_name = 'about'

urlpatterns = [
    # path函数将url映射到视图
    path('', views.about),

]