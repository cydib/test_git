from django.db import models
from project_app.models import Module


# Create your models here.
class TestCase(models.Model):
    '''
    用例表
    '''

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("用例名称", max_length=100, blank=False, default="")
    url = models.TextField("请求url", default="")
    req_method = models.CharField("请求方法", max_length=10, default="")
    par_type = models.CharField("参数类型", max_length=10, default="")
    req_headers = models.TextField("header", default="")
    req_parameter = models.TextField("参数", default="")
    req_assert = models.TextField("验证", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    # 在admin后台显示创建时的标题，而不是project1、2
    def __str__(self):
        return self.name
