from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep
from django.contrib.auth.models import User
from project_app.models import Module, Project
from selenium.common.exceptions import NoSuchElementException


class TestModule(StaticLiveServerTestCase):
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
        p = Project.objects.get(name="test项目")
        Module.objects.create(project_id=p.id, name="test模块", describe="test模块描述")
        self.driver.get('%s%s' % (self.live_server_url, "/"))
        username = self.driver.find_element_by_name("username")
        username.send_keys("admin")
        password = self.driver.find_element_by_name("password")
        password.send_keys("admin123456")
        self.driver.find_element_by_xpath("/html/body/div/form/button").click()
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div/div/div[1]/ul[1]/li[2]/a").click()
        sleep(1)

    def test_add_module(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/button").click()
        self.driver.find_element_by_name("project").find_element_by_xpath('//*[@id="id_project"]/option[2]').click()
        self.driver.find_element_by_name("name").send_keys("ui自动化测试-输入模块名称")
        self.driver.find_element_by_name("describe").send_keys("ui自动化测试-输入模块描述")
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/form/button[2]").click()
        sleep(1)
        module_name = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[2]/td[2]").text
        self.assertEqual(module_name, "ui自动化测试-输入模块名称")
        module_describe = self.driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/div/table/tbody/tr[2]/td[3]").text
        self.assertEqual(module_describe, "ui自动化测试-输入模块描述")

    def test_update_module(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[6]/a").click()
        self.driver.find_element_by_name("project").find_element_by_xpath('//*[@id="id_project"]/option[2]').click()
        self.driver.find_element_by_name("name").send_keys("ui自动化测试-输入模块名称")
        self.driver.find_element_by_name("describe").send_keys("ui自动化测试-输入模块描述")
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/form/button[2]").click()
        sleep(1)
        module_name = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[2]").text
        self.assertEqual(module_name, "test模块ui自动化测试-输入模块名称")
        module_describe = self.driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[3]").text
        self.assertEqual(module_describe, "test模块描述ui自动化测试-输入模块描述")

    def test_dele_module(self):
        self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[7]/a").click()
        self.driver.switch_to.alert.accept()
        try:
            module_name = self.driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[2]").text
        except NoSuchElementException:
            module_name = ""

        try:
            module_describe = self.driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/table/tbody/tr[1]/td[4]").text
        except NoSuchElementException:
            module_describe = ""

        self.assertEqual(module_name, "")
        self.assertEqual(module_describe, "")
