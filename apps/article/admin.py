from django.contrib import admin

from .models import ArticlePost

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.userprofile.models import Profile

from .models import ArticleColumn

from .models import ArticleCourse

# Register your models here.

# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.register(ArticlePost)

admin.site.unregister(User)

admin.site.register(ArticleColumn)
admin.site.register(ArticleCourse)

admin.site.register(User, UserAdmin)
# 注册文章栏目
