from interface_app.models import TestCase, TestTask
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
                    case_dict = {
                        "id": c.id,
                        "name": case_info
                    }
                    cases_list.append(case_dict)

        return common.response_succeed(data=cases_list)
    else:
        return common.response_failed("请求方法错误")


def get_task_info(request):
    """
    获取任务详情
    :param request:
    :return:
    """
    if request.method == "GET":
        task_id = request.GET.get("taskId", "")
        print("task_id", task_id)
        try:
            task_obj = TestTask.objects.get(pk=task_id)
        except TestTask.DoesNotExist:
            return common.response_failed("任务不存在")

        task_name = task_obj.name
        task_des = task_obj.describe
        task_status = task_obj.status
        task_case = task_obj.cases

        task_info = {
            "task_Id": task_id,
            "task_name": task_name,
            "task_des": task_des,
            "task_status": task_status,
            "task_case": task_case,
        }

        return common.response_succeed(data=task_info)

    else:
        return common.response_failed("请求方法错误")
