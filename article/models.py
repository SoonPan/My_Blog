from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User
#timezone 用于处理时间相关的事物
from django.utils import timezone

from taggit.managers import TaggableManager

from PIL import Image

from django.urls import reverse
#博客的文章数据模型

class ArticleColumn(models.Model):

    title = models.CharField(max_length=100,blank=True)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title





class ArticlePost(models.Model):
    #文章作者，on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=120)

    body = models.TextField()

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 文章标签
    tags = TaggableManager(blank=True)

    total_views = models.PositiveIntegerField(default=0)

    #文章的创作时间
    created = models.DateTimeField(default=timezone.now)
    #文章最后的修改时间
    updated = models.DateTimeField(auto_now=True)

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )



    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])


    #内部类定义元数组
    class Meta:
        #ordering 指定文章模型的返回排列顺序
        #‘-created’ 表示倒序排列
        ordering = ('-created',)

    #当文章对象被打印时，返回文章的标题
    def __str__(self):

        return self.title