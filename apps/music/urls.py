# 引入path
from django.urls import path
from apps.music import views

# 正在部署的应用的名称
app_name = 'music'

urlpatterns = [
    # path函数将url映射到视图
    path('', views.music),

]