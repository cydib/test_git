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

