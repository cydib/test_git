from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from test_platform import common
from interface_app.models import TestCase, TestTask
from project_app.models import Project, Module
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def task_manage(request):
    tasks = TestTask.objects.all()
    paginator = Paginator(tasks, 10)
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
        return render(request, "task_manage.html", {"type": "add_task"})


@login_required
def save_task(request):
    if request.method == "POST":
        task_name = request.POST.get("task_name", "")
        task_describe = request.POST.get("task_describe", "")
        task_case = request.POST.get("task_cases", "")
        task_status = request.POST.get("task_status", "")

        if task_name == "":
            return common.response_failed("任务名称不能为空")
        TestTask.objects.create(name=task_name, describe=task_describe, cases=task_case, status=task_status)
        return common.response_succeed("任务创建成功")
    else:
        return common.response_failed("请求方法不正确")


@login_required
def edit_task(request, tid):
    return render(request, "task_manage.html", {"type": "edit_task"})


@login_required
def update_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id", "")
        task_name = request.POST.get("task_name", "")
        task_describe = request.POST.get("task_describe", "")
        task_case = request.POST.get("task_cases", "")

        if task_name == "" or task_id == "":
            return common.response_failed("任务ID或名称不能为空")

        task_obj = TestTask.objects.select_for_update().filter(id=task_id).update(name=task_name,
                                                                                  describe=task_describe,
                                                                                  cases=task_case, )
        if task_obj == 1:
            return common.response_succeed("更新成功！")
        else:
            return common.response_failed("更新失败！")
    else:
        return common.response_failed("请求方法错误")


@login_required
def delete_task(request, tid):
    TestTask.objects.get(id=tid).delete()
    return HttpResponseRedirect('/interface/task_manage/')
