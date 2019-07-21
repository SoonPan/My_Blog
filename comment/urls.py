from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),

    path('confirm_delete/<int:article_id>/<int:comment_id>/<int:flag>', views.comment_delete, name='comment_delete'),

    path('edit-comment/<int:article_id>/<int:comment_id>', views.edit_comment, name='edit_comment'),
]