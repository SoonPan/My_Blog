# Generated by Django 2.1 on 2019-08-10 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20190810_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='summary',
            field=models.TextField(default='文章摘要等同于网页description内容，请务必填写...', max_length=230, verbose_name='文章摘要'),
        ),
    ]