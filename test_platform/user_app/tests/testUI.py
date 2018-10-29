#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 22:34:42
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep


# Create your tests here.


class LoginTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_null(self):
        self.driver.get('%s%s' % (self.live_server_url, "/"))
        username = self.driver.find_element_by_name("username")
        username.send_keys("")
        password = self.driver.find_element_by_name("password")
        password.send_keys("")
        self.driver.find_element_by_xpath("/html/body/div/form/button").click()
        error_text = self.driver.find_element_by_xpath("/html/body/div/form/p").text
        sleep(2)
        self.assertEquals("用户名或密码不能为空", error_text)
