from interface_app.models import TestCase
from project_app.models import Project, Module
from test_platform import common


def get_case_list(request):
    """
   获取测试用例列表
   :param request:
   :return:
   """
    if request.method == "GET":
        cases_list = []
        projects = Project.objects.all()
        for p in projects:
            modules = Module.objects.filter(project_id=p.id)
            for m in modules:
                cases = TestCase.objects.filter(module_id=m.id)
                for c in cases:
                    case_info = p.name + " -> " + m.name + " -> " + c.name
                    cases_list.append(case_info)

        return common.response_succeed(data=cases_list)
    else:
        return common.response_failed("请求方法错误")