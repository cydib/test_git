import json
import requests

from test_platform import common
from interface_app.models import TestCase
from project_app.models import Project, Module
from django.contrib.auth.decorators import login_required


@login_required
def get_porject_list(request):
    """
    获取项目模块列表
    :param request:
    :return: 项目接口列表
    """
    if request.method == "GET":
        project_list = Project.objects.all()
        data_list = []
        for project in project_list:
            project_dict = {
                "name": project.name
            }
            module_list = Module.objects.filter(project_id=project.id)
            if len(module_list) != 0:
                module_name = []
                for module in module_list:
                    module_name.append(module.name)

                project_dict["moduleList"] = module_name
                data_list.append(project_dict)

        return common.response_succeed(data=data_list)
    else:
        return common.response_failed("请求方法错误")


@login_required
def get_case_info(request):
    """
   获取接口数据
   :param request:
   :return:
   """
    if request.method == "POST":
        case_id = request.POST.get("caseId", "")
        if case_id == "":
            return common.response_failed("用例ID不能为空")

        try:
            case_obj = TestCase.objects.get(pk=case_id)
        except TestCase.DoesNotExist:
            return common.response_failed("用例不存在")

        module_obj = Module.objects.get(id=case_obj.module_id)
        module_name = module_obj.name

        project_name = Project.objects.get(id=module_obj.project_id).name

        case_info = {
            "moduleName": module_name,
            "projectName": project_name,
            "name": case_obj.name,
            "url": case_obj.url,
            "reqMethod": case_obj.req_method,
            "reqType": case_obj.par_type,
            "reqHeader": case_obj.req_headers,
            "reqParameter": case_obj.req_parameter,
            "assertText": case_obj.req_assert,
        }

        return common.response_succeed(data=case_info)

    else:
        return common.response_failed("请求方法错误")
