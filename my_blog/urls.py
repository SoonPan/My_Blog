"""our my_blog URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from article.views import article_list


import notifications.urls


urlpatterns = [
    path('adminspock/', admin.site.urls),

    path('', article_list, name='home'),

    path('article/', include('article.urls', namespace='article')),

    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),

    path('password-reset/', include('password_reset.urls')),

    # 评论
    path('comment/', include('comment.urls', namespace='comment')),

    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('notice/', include('notice.urls', namespace='notice')),

    path('accounts/', include('allauth.urls')),

    path('tech/', include('tech.urls')),
    path('life/', include('life.urls')),
    path('book&moive/', include('bookmoive.urls')),
    path('music/', include('music.urls')),
    path('about/', include('about.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
