import json
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
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


@login_required
def run_task(request, tid):
    if request.method == "GET":
        task_obj = TestTask.objects.get(id=tid)
        cases_list = task_obj.cases.split(",")
        cases_list.pop()

        task_obj.status = 1
        task_obj.save()

        all_cases_list = {}
        for case in cases_list:
            case_obj = TestCase.objects.get(id=case)
            case_dict = {
                "url": case_obj.url,
                "method": case_obj.req_method,
                "type_": case_obj.par_type,
                "headers": case_obj.req_headers,
                "parameter": case_obj.req_parameter,
                "assert_": case_obj.req_assert
            }
            all_cases_list[case_obj.id] = case_dict
        print(all_cases_list)
        cases_str = json.dumps(all_cases_list)

        cases_data_file = TASK_PATH + "cases_data.json"
        print(cases_data_file)

        with open(cases_data_file, "w+") as f:
            f.write(cases_str)

        # 运行测试
        os.system("py " + RUN_TASK_FILE)

        return HttpResponseRedirect("/interface/task_manage")
    else:
        return HttpResponse("404")
