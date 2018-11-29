from django.contrib import admin

# Register your models here.
from django.contrib import admin
from interface_app.models import TestCase, TestTask


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'req_method',
                    'par_type', 'req_headers', 'req_parameter', 'req_assert']


class TestTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'cases', 'status']


admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestTask, TestTaskAdmin)