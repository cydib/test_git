from django.test import TestCase
from project_app.models import Project
from django.contrib.auth.models import User


# Create your tests here.

class ProjectTest(TestCase):

    def setUp(self):
        User.objects.create_user("test", "test@mail.com", "test1234")
        Project.objects.create(name="test项目", describe="test描述")
        data = {"username": "test", "password": "test1234"}
        self.client.post('/login_action/', data=data)

    def testProject(self):
        respone = self.client.post('/manage/project_manage/')
        project_html = respone.content.decode('utf-8')
        self.assertEqual(respone.status_code, 200)
        self.assertIn("test项目", project_html)
        self.assertIn("test描述", project_html)

    def test_create_project(self):
        data = {"name": "测试项目名称", "describe": "测试项目描述", "status": "on"}
        r = self.client.post('/manage/add_project/', data=data)
        project_name = Project.objects.get(name="测试项目名称")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(project_name.name, "测试项目名称")

    def test_update_project(self):
        project_name = Project.objects.get(name="test项目")
        data = {"name": "修改测试项目名称", "describe": "修改测试项目描述", "status": "off"}
        r = self.client.post('/manage/edit_project/' + str(project_name.id) + "/", data=data)
        project_new_name = Project.objects.get(name="修改测试项目名称")
        self.assertEqual(project_new_name.name, "修改测试项目名称")

    def test_dele_project(self):
        project_name = Project.objects.get(name="test项目")
        r = self.client.get('/manage/del_project/' + str(project_name.id) + "/")
        self.assertEqual(r.status_code, 302)
