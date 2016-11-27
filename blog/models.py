# coding:utf-8
from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=128, default='anonymous', editable=False, verbose_name="描述")
    # content = models.TextField(blank=True, null = True,verbose_name = "文章内容")
    Content = UEditorField('文章内容', height=100, width=500, toolbars='normal', blank=True, imagePath="image/",)

    create_date = models.DateTimeField(auto_now_add=False, verbose_name="创建时间")
    modify_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    is_original = models.BooleanField(default=False, verbose_name="是否原创")
    is_publish = models.BooleanField(default=True, verbose_name="是否推荐")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
