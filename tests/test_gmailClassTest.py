
import base64, email
import sys
import pytest

from apiclient import discovery
from httplib2 import Http
from apiclient import errors

sys.path.insert(0, '/home/kashyap/PycharmProjects/surveymonkey/classes')

from gmailClass import EmailReader


class TestGmailReader:
    """
        Class to test the Gmail Reader
    """

    # Fixture to create email object which validates the GMAIL credentials of the user
    @pytest.fixture(scope='module')
    def objectCreation(self) :
        emailObj = EmailReader(email)
        assert emailObj != ''
        return emailObj

    # Fixture to create JSON object of the emails based on the search parameters
    @pytest.fixture(scope='module')
    def messageCreation(self,objectCreation):
        emailObj = objectCreation
        service = discovery.build('gmail', 'v1', http=emailObj.creds.authorize(Http()))
        messages = emailObj.ListMessagesMatchingQuery(service, 'me', 'from:surveymonkey.com')
        return messages

    def setup_method(self, objectCreation):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

    def teardown_method(self, objectCreation):
        """ teardown any state that was previously setup with a setup_method
        call.
        """

    # Test case to validate GMAIL credentials (object creation)
    def test_OjbectCreation(self,objectCreation,capsys):
        emailObj = objectCreation
        capsys.disabled()
        print('this output is captured')
        # with capsys.disabled():
        #     print('output not captured, going directly to sys.stdout')
        print('this output is also captured')
        assert emailObj != ''

    # Test case to validate email messages recieved based on the searc parameters
    def test_messageCreation(self,objectCreation,messageCreation):
        messages = messageCreation
        assert messages != ''

    # Test case to validate survey title
    def test_getSurveyTitle(self,objectCreation,messageCreation):
        emailObj = objectCreation
        messages = messageCreation
        headerVar, surveyTitle, surveyLogo, surveyPara, surveyFirstQuestion = emailObj.getEmailParts(messages)
        assert surveyTitle != ''

    # Test case to validate survey logo
    def test_getSurveyLogo(self, objectCreation, messageCreation):
        emailObj = objectCreation
        messages = messageCreation
        headerVar, surveyTitle, surveyLogo, surveyPara, surveyFirstQuestion = emailObj.getEmailParts(messages)
        assert (surveyLogo != '')

    # Test case to validate survey introduction paragraph
    def test_getSurveyPara(self, objectCreation, messageCreation):
        emailObj = objectCreation
        messages = messageCreation
        headerVar, surveyTitle, surveyLogo, surveyPara, surveyFirstQuestion = emailObj.getEmailParts(messages)
        assert surveyPara != ''

    # Test case to validate survey question
    def test_getSurveyFirstQuestion(self, objectCreation, messageCreation):
        emailObj = objectCreation
        messages = messageCreation
        headerVar, surveyTitle, surveyLogo, surveyPara, surveyFirstQuestion = emailObj.getEmailParts(messages)
        assert surveyFirstQuestion != ''

# email = gmailClass.EmailReader(email)
# threads = email.getEmailList()
# headerVar,surveyTitle,surveyLogo,surveyPara,surveyFirstQuestion = email.getEmailParts(threads)
# service = discovery.build('gmail', 'v1', http=email.creds.authorize(Http()))
# messages = email.ListMessagesMatchingQuery(service,'me','from:surveymonkey.com')
#
# print(messages)
# for msg in messages:
#     print(msg)
# print('----')
# print(headerVar)
# print('Survey Title Is : '+surveyTitle)
# print('Survey Logo Is : '+surveyLogo)
# print('Survey Paragraph Is : '+surveyPara)
# print('Survey Question Is : '+surveyFirstQuestion)