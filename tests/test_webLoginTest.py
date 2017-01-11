import time
import sys
import pytest

from apiclient import discovery
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

sys.path.insert(0, '/home/kashyap/PycharmProjects/surveymonkey/resources')

from variables import Variables


class TestWebLogin:
    """
        Class to test the Google login functionality
    """
    # def __init__(self,email):
    #     self.baseUrl = '';
    #     self.userEmail = '';
    #     self.userPassword = '';
    #     self.browser = '';

    @pytest.fixture(scope='module')
    def objectCreation(self):
        b = Variables()
        self.baseUrl,self.userEmail,self.userPassword,self.browser = b.varReturnFunc();
        assert b.varReturnFunc() != '';
        if self.browser == 'Firefox':
            assert self.browser == 'Firefox';
            self.browser = webdriver.Remote(
                command_executor='http://192.168.4.37:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            )

            #self.browser = webdriver.Firefox();
        #assert str(type(self.browser)) == '<class \'selenium.webdriver.firefox.webdriver.WebDriver\'>'
        return self.baseUrl,self.userEmail,self.userPassword,self.browser;

    def test_objectCreation(self,objectCreation):
        self.baseUrl,self.userEmail,self.userPassword,self.browser = objectCreation;
        assert self.baseUrl != '';
        assert self.browser != '';

    def test_gmailLogin(self, objectCreation):
        self.baseUrl, self.userEmail, self.userPassword, self.browser = objectCreation;
        self.browser.get(self.baseUrl);
        self.browser.maximize_window();
        # self.browser.set_script_timeout(10);
        time.sleep(5);
        self.browser.find_element_by_id('hlGoogle').click();
        #self.browser.set_script_timeout(10);
        time.sleep(10);
        self.browser.find_element_by_id('Email').send_keys(self.userEmail);
        self.browser.find_element_by_id('next').click();
        time.sleep(10);
        self.browser.find_element_by_id('Passwd').send_keys('');
        self.browser.find_element_by_id('signIn').click();
        time.sleep(10);
        self.openSurvey();
        assert self.browser.find_element_by_id('hd') != '';

    def openSurvey(self):
        self.browser.find_elements_by_tag_name('data-location','summary').click();