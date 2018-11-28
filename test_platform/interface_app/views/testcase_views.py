import requests, json
from test_platform import common
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from project_app.models import Project, Module
from interface_app.models import TestCase
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def case_manage(request):
    testcases = TestCase.objects.all()
    paginator = Paginator(testcases, 10)
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
        testcase = TestCase.objects.all()
        return render(request, "case_manage.html", {"type": "list", "testcases": contacts})
    else:
        return HttpResponse("404")


def add_case(request):
    if request.method == "GET":
        return render(request, "add_case.html", {"type": "add_case"})
    else:
        return HttpResponse("404")


def debug_case(request):
    if request.method == "POST":
        url = request.POST.get("req_url")
        method = request.POST.get("req_method")
        parameter = request.POST.get("req_parameter")

        # payload = json.loads(parameter.replace("'", "\""))
        if method == "get":
            r = requests.get(url)
            r.encoding = "utf-8"

        if method == "post":
            r = requests.post(url, data=parameter)
            r.encoding = "utf-8"
            r = requests.post(url, data=parameter, verify=False)

        return HttpResponse(r.text)


def save_case(request):
    """
    保存测试用例
    """
    if request.method == "POST":
        name = request.POST.get("name", "")
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method", "")
        parameter = request.POST.get("req_parameter", "")
        req_type = request.POST.get("req_type", "")
        header = request.POST.get("header", "")
        module_name = request.POST.get("module", "")
        assert_text = request.POST.get("assert", "")

        if url == "" or method == "" or req_type == "" or module_name == "":
            return HttpResponse("必传参数为空")

        if parameter == "":
            parameter = "{}"

        if header == "":
            header = "{}"

        module_obj = Module.objects.get(name=module_name)

        case = TestCase.objects.create(name=name, module=module_obj, url=url,
                                       req_method=method, req_headers=header,
                                       par_type=req_type,
                                       req_parameter=parameter,
                                       req_assert=assert_text)
        if case is not None:
            return HttpResponse("保存成功！")

    else:
        return HttpResponse("404")


def search_case_name(request):
    if request.method == "GET":
        case_name = request.GET.get("case_name", "")
        case = TestCase.objects.filter(name__contains=case_name)

        paginator = Paginator(case, 10)
        page = request.GET.get('page')

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, "case_manage.html", {
            "type": "list",
            "testcases": contacts,
            "case_name": case_name,
        })
    else:
        return HttpResponse("404")


def edit_case(request, cid):
    if request.method == "GET":
        return render(request, "edit_case.html", {
            "type": "edit_case"})
    else:
        return HttpResponse("404")


def update_case(request):
    if request.method == "POST":
        cid = request.POST.get("cid")
        # print("cid", cid)
        name = request.POST.get("name")
        url = request.POST.get("req_url")
        method = request.POST.get("req_method")
        parameter = request.POST.get("req_parameter")
        req_type = request.POST.get("req_type")
        header = request.POST.get("header")
        module_name = request.POST.get("module")
        req_assert = request.POST.get("assert")

        if url == "" or method == "" or req_type == "" or module_name == "":
            return common.response_failed("必传参数为空")

        if parameter == "":
            parameter = "{}"

        if header == "":
            header = "{}"

        module_obj = Module.objects.get(name=module_name)
        case_obj = TestCase.objects.select_for_update().filter(id=cid).update(name=name,
                                                                              url=url, req_method=method,
                                                                              req_assert=req_assert,
                                                                              par_type=req_type,
                                                                              req_headers=header,
                                                                              module=module_obj,
                                                                              req_parameter=parameter)
        if case_obj == 1:
            return common.response_succeed("更新成功！")
        else:
            return common.response_failed("更新失败！")
    else:
        return common.response_failed("请求方法错误")


def del_case(request, cid):
    TestCase.objects.get(id=cid).delete()
    return HttpResponseRedirect('/interface/case_manage/')


def api_assert(request):
    if request.method == "POST":
        result = request.POST.get("result", "")
        assert_text = request.POST.get("assert", "")

        if result == "" or assert_text == "":
            return common.response_failed("验证的数据不能为空")

        try:
            assert assert_text in result
        except AssertionError:
            return common.response_failed("验证失败")
        else:
            return common.response_succeed("验证通过")
    else:
        return common.response_failed("请求方法错误")
