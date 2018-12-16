import os
import json
import threading
from time import sleep
from interface_app.models import TestTask
from interface_app.models import TestCase
from interface_app.models import TestResult
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
from xml.dom import minidom


class TaskThread():
    """实现测试任务的多线程执行"""

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self, tid):
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

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_cases, args=(self.tid,))
        threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        sleep(2)
        print("当（任务）线程运行完成之后...")
        self.save_result()

        task_obj = TestTask.objects.get(id=self.tid)
        task_obj.status = 2  # 修改状态执行完成
        task_obj.save()

    def new_run(self):
        threads = []
        t = threading.Thread(target=self.run)
        threads.append(t)

        for t in threads:
            t.start()

    def save_result(self):
        """
        保存测试结果
        """
        dom = minidom.parse(TASK_PATH + 'results.xml')
        root = dom.documentElement
        ts = root.getElementsByTagName('testsuite')
        print(ts)
        errors = ts[0].getAttribute("errors")
        failures = ts[0].getAttribute("failures")
        skipped = ts[0].getAttribute("skipped")
        tests = ts[0].getAttribute("tests")
        name = ts[0].getAttribute("name")
        run_time = ts[0].getAttribute("time")

        with open(TASK_PATH + 'results.xml', "r", encoding="utf-8") as f:
            result_text = f.read()

        print(type(result_text))
        print(result_text)

        print("errors", ts[0].getAttribute("errors"))
        print("fail", ts[0].getAttribute("failures"))
        print("tests", ts[0].getAttribute("tests"))

        ret = TestResult.objects.create(name=name,
                                        error=errors,
                                        failure=failures,
                                        skipped=skipped,
                                        tests=tests,
                                        task_id=self.tid,
                                        run_time=run_time,
                                        result=result_text)  # 保存到结果表里面
        print(ret)
