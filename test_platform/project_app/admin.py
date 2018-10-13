from django.contrib import admin
from project_app.models import Project, Module

# Register your models here.



# Register your models here.

# 将数据库的字段展示到admin后台
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'status', 'create_time', 'id']


class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'create_time', 'describe']


# 将数据库的表展示到admin后台
admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)
