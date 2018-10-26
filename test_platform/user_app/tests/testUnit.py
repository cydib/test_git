from django.test import TestCase
from django.contrib.auth.models import User


class UserModelsTest(TestCase):
    '''
    测试数据库模型
    '''

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test1232456")

    def test_create_user(self):
        '''
        验证创建功能
        '''
        User.objects.create_user("test02", "test02@mail.com", "testqwer")
        user = User.objects.get(username="test02")
        self.assertEqual(user.username, "test02")
        self.assertEqual(user.email, "test02@mail.com")

    def test_query_user(self):
        '''
        验证查询功能
        '''
        user = User.objects.get(username="test01")
        self.assertEqual(user.username, "test01")
        self.assertEqual(user.email, "test01@mail.com")

    def test_update_user(self):
        '''
        验证修改功能
        '''
        user = User.objects.get(username="test01")
        user.username = "uptate_test"
        user.email = 'update_test02@mail.com'
        user.save()
        user1 = User.objects.get(username="uptate_test")
        self.assertEqual(user1.username, "uptate_test")
        self.assertEqual(user1.email, "update_test02@mail.com")

    def test_dele_user(self):
        '''
        验证删除功能
        '''
        user = User.objects.get(username="test01")
        user.delete()
        user = User.objects.filter(username="test01")
        self.assertEqual(len(user), 0)


class TestHomePage(TestCase):
    '''
    测试首页
    '''

    def testHomepage(self):
        respone = self.client.get("/")
        self.assertEqual(respone.status_code, 200)
        self.assertTemplateUsed(respone, "index.html")


class LoginActionTest(TestCase):
    '''
    测试登录页面
    '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_user(self):
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_username_psswd_is_empty(self):
        respone = self.client.post('/login_action/', {"username": "", "password": ""})
        login_html = respone.content.decode('utf-8')
        self.assertEqual(respone.status_code, 200)
        self.assertIn("用户名或密码不能为空", login_html)

    def test_username_psswd_is_error(self):
        respone = self.client.post('/login_action/', {"username": "admin", "password": "admin"})
        login_html = respone.content.decode('utf-8')
        self.assertEqual(respone.status_code, 200)
        self.assertIn("用户名或密码错误", login_html)

    def test_login_success(self):
        respone = self.client.post('/login_action/', {"username": "admin", "password": "admin123456"})
        login_html = respone.content.decode('utf-8')
        self.assertEqual(respone.status_code, 302)
