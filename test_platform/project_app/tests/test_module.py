from django.test import TestCase
from project_app.models import Module, Project
from django.contrib.auth.models import User


class ModuleTest(TestCase):

    def setUp(self):
        User.objects.create_user("test", "test@mail.com", "test1234")
        Project.objects.create(name="test项目", describe="test描述")
        self.p = Project.objects.get(name="test项目")
        Module.objects.create(project_id=self.p.id, name="test模块123", describe="test模块描述123")
        data = {"username": "test", "password": "test1234"}
        self.client.post('/login_action/', data=data)

    def testModule(self):
        respone = self.client.post("/manage/module_manage/")
        module_html = respone.content.decode('utf-8')
        self.assertIn("test模块123", module_html)
        self.assertIn("test模块描述123", module_html)

    def test_create_module(self):
        data = {"project": self.p.id, "name": "测试模块名称", "describe": "测试模块描述"}
        r = self.client.post('/manage/add_module/', data=data)
        module_name = Module.objects.get(name="测试模块名称")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(module_name.name, "测试模块名称")

    def test_update_module(self):
        module_name = Module.objects.get(name="test模块123")
        data = {"project": self.p.id, "name": "修改测试模块名称", "describe": "修改测试模块描述"}
        r = self.client.post('/manage/edit_module/' + str(module_name.id) + "/", data=data)
        module_new_name = Module.objects.get(name="修改测试模块名称")
        self.assertEqual(module_new_name.name, "修改测试模块名称")

    def test_dele_module(self):
        module_name = Module.objects.get(name="test模块123")
        r = self.client.get('/manage/del_module/' + str(module_name.id) + "/")
        self.assertEqual(r.status_code, 302)