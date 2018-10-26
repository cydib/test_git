from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep
# Create your tests here.


class LoginTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_null(self):
        self.selenium.get('%s%s' %(self.live_server_url, "/"))
        username = self.selenium.find_element_by_name("username")
        username.send_keys("")
        password = self.selenium.find_element_by_name("password")
        password.send_keys("")
        self.selenium.find_element_by_id("loginButton").click()
        error_text = self.selenium.find_element_by_id("error").text
        sleep(2)
        self.assertEquals("用户名或密码不能为空", error_text)