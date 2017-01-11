from __future__ import print_function
from bs4 import BeautifulSoup
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64, email
from apiclient import errors
import string

class EmailReader:
    """Class for email verification"""

    # Function for initializing google API
    def __init__(self,email) :

        self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        self.store = file.Storage('../resources/storage.json')
        self.creds = self.store.get()
        self.GMAIL = discovery.build('gmail', 'v1', http=self.creds.authorize(Http()))
        self.emailMsg = email.message_from_string
        print("Class for email manipulation")

    # Function for fetching query based emails
    def ListMessagesMatchingQuery(self,service, user_id, query='') :
        try:
            response = self.GMAIL.users().messages().list(userId=user_id,q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError, error:
            print('An error occurred: %s' % error)

    # Function for fetching email threads
    def getEmailList(self) :

        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets('../resources/client_secret.json', self.SCOPES)
            self.creds = tools.run_flow(flow, self.store)
            self.GMAIL = discovery.build('gmail', 'v1', http=self.creds.authorize(Http()))
        threads = self.GMAIL.users().threads().list(userId='me').execute().get('threads', [])
        return threads

    # Function for extracting email contents
    def getEmailParts(self, threads) :

        for thread in threads:
            # msgId = thread['id']
            msgId = '15916a1d838aef04'
            message = self.GMAIL.users().messages().get(userId='me', id=msgId, format='full').execute()

            msgStr = base64.urlsafe_b64decode(message['payload']['body']['data'].encode('ASCII'))
            msgStr = self.emailMsg(msgStr)
            msgStr = str(msgStr)

            headerVar = message['payload']['headers']
            headerVar = {headerVar[i]['name']: headerVar[i]['value'] for i, k in enumerate(headerVar)}

            msgStr = BeautifulSoup(msgStr, "html5lib")
            surveyTitle = msgStr.find("td",style="font-size: 29px; color:#FFFFFF; font-weight: normal; letter-spacing: 1px; line-height: 1;\n                           "
                                    "text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.2); font-family: Arial,Helvetica,sans-serif;")
            surveyTitle = surveyTitle.text.strip()

            surveyLogo = msgStr.find("img", alt="SurveyMonkey Logo")
            surveyLogo = surveyLogo['src'].strip()

            surveyPara = msgStr.select("tr:nth-of-type(5)")[0]
            surveyPara = surveyPara.find('td', style='color:#666666; font-size: 13px;').text.strip()

            surveyFirstQuestion = msgStr.select("tr:nth-of-type(8)")[0]
            surveyFirstQuestion = surveyFirstQuestion.find('td',style="word-wrap: break-word;white-space: normal;font-size: 24px;font-family: helvetica neue,helvetica,arial,sans-serif;font-weight: 300;line-height: 30px;color: #4DB2EC;font-style: normal;text-decoration: none;").text

            return headerVar,surveyTitle,surveyLogo,surveyPara,surveyFirstQuestion

email = EmailReader(email)
threads = email.getEmailList()
headerVar,surveyTitle,surveyLogo,surveyPara,surveyFirstQuestion = email.getEmailParts(threads)
service = discovery.build('gmail', 'v1', http=email.creds.authorize(Http()))
messages = email.ListMessagesMatchingQuery(service,'me','from:surveymonkey.com')

print(messages)
for msg in messages:
    print(msg)
print('----')
print(headerVar)
print('Survey Title Is : '+surveyTitle)
print('Survey Logo Is : '+surveyLogo)
print('Survey Paragraph Is : '+surveyPara)
print('Survey Question Is : '+surveyFirstQuestion)