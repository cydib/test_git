from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from test_platform import common
from interface_app.models import TestCase, TestTask
from project_app.models import Project, Module
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def task_manage(request):
    tasks = TestTask.objects.all()
    paginator = Paginator(tasks, 5)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    if request.method == "GET":
        return render(request, "task_manage.html", {"type": "list", "tasks": contacts})

@login_required
def add_task(request):
    if request.method == "GET":
        return render(request, "add_task.html", {"type": "add_task"})


@login_required
def save_task(request):
    if request.method == "POST":
        task_name = request.POST.get("task_name", "")
        task_describe = request.POST.get("task_describe", "")
        task_case = request.POST.get("task_cases", "")
        task_status = request.POST.get("task_status", "")

        if task_name == "":
            return common.response_failed("任务名称不能为空")
        TestTask.objects.create(name=task_name, describe=task_describe, cases=task_case,status=task_status)
        return common.response_succeed("成功")
    else:
        return common.response_failed("请求方法不正确")
