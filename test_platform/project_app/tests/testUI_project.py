from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep
from django.contrib.auth.models import User
from project_app.models import Project
from selenium.common.exceptions import NoSuchElementException


class TestProject(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="test项目", describe="test描述")
        self.driver.get('%s%s' % (self.live_server_url, "/"))
        username = self.driver.find_element_by_name("username")
        username.send_keys("admin")
        password = self.driver.find_element_by_name("password")
        password.send_keys("admin123456")
        self.driver.find_element_by_xpath("/html/body/div/form/button").click()
        sleep(2)

    def test_add_project(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/button").click()
        self.driver.find_element_by_name("name").send_keys("ui自动化测试-输入项目名称")
        self.driver.find_element_by_name("describe").send_keys("ui自动化测试-输入项目描述")
        self.driver.find_element_by_id("id_status").click()
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/form/button[2]").click()
        sleep(1)
        project_name = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[2]/td[2]").text
        self.assertEqual(project_name, "ui自动化测试-输入项目名称")
        project_describe = self.driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/div/table/tbody/tr[2]/td[4]").text
        self.assertEqual(project_describe, "ui自动化测试-输入项目描述")

    def test_update_project(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[6]/a").click()
        self.driver.find_element_by_name("name").send_keys("ui自动化测试-输入项目名称")
        self.driver.find_element_by_name("describe").send_keys("ui自动化测试-输入项目描述")
        self.driver.find_element_by_id("id_status").click()
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/form/button[2]").click()
        sleep(1)
        project_name = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[2]").text
        self.assertEqual(project_name, "test项目ui自动化测试-输入项目名称")
        project_describe = self.driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[4]").text
        self.assertEqual(project_describe, "test描述ui自动化测试-输入项目描述")

    def test_dele_project(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[7]/a").click()
        self.driver.switch_to.alert.accept()
        try:
            project_name = self.driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[2]").text
        except NoSuchElementException:
            project_name = ""

        try:
            project_describe = self.driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[4]").text
        except NoSuchElementException:
            project_describe = ""

        self.assertEqual(project_name, "")
        self.assertEqual(project_describe, "")
