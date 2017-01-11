from __future__ import print_function
from bs4 import BeautifulSoup
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64, email
import string

def getEmailConfig():
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('storage.json')
    creds = store.get()
    return creds,SCOPES,store

def getEmailList():
    creds,SCOPES,store = getEmailConfig()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../resources/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    threads = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
    return threads,GMAIL

def getEmailParts(threads):
    for thread in threads:
        #msgId = thread['id']
        msgId = '15916a1d838aef04'
        tdata = GMAIL.users().threads().get(userId='me', id=thread['id']).execute()
        nmsgs = len(tdata['messages'])
        message = GMAIL.users().messages().get(userId='me', id=msgId, format='full').execute()

        msgStr = base64.urlsafe_b64decode(message['payload']['body']['data'].encode('ASCII'))
        msgStr = email.message_from_string(msgStr)
        msgStr = str(msgStr)

        headerVar = message['payload']['headers']
        headerVar = {headerVar[i]['name']: headerVar[i]['value'] for i, k in enumerate(headerVar)}
        print(headerVar)
        # for key,val in headerVar.iteritems():
        #     print (key+'--->'+val);
        # break
        msgStr = BeautifulSoup(msgStr, "html5lib")
        surveyTitle = msgStr.find("td",style="font-size: 29px; color:#FFFFFF; font-weight: normal; letter-spacing: 1px; line-height: 1;\n                           "
                            "text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.2); font-family: Arial,Helvetica,sans-serif;")
        surveyTitle = surveyTitle.text
        #print(msgStr.prettify())
        surveyLogo = msgStr.findlsub("img", alt="SurveyMonkey Logo")
        surveyLogo = surveyLogo['src']

        surveyPara = msgStr.select("tr:nth-of-type(5)")[0]
        surveyPara = surveyPara.find('td',style='color:#666666; font-size: 13px;').text

        surveyFirstQuestion = msgStr.select("tr:nth-of-type(8)")[0]
        surveyFirstQuestion = surveyFirstQuestion.find('td', style="word-wrap: break-word;white-space: normal;font-size: 24px;font-family: helvetica neue,helvetica,arial,sans-serif;font-weight: 300;line-height: 30px;color: #4DB2EC;font-style: normal;text-decoration: none;").text

        print(surveyTitle)
        print(surveyLogo)
        print(surveyPara)
        print(surveyFirstQuestion)

        break

threads, GMAIL = getEmailList()
getEmailParts(threads)