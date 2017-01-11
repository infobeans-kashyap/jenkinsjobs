class Variables(object):
    baseUrl = 'https://www.surveymonkey.com/user/sign-in/?ep=%2Fanalyze%2FIgFm2mJ8lMq2a3EmjD_2Be1sDxcZYQCheVnCp7R7ftri4_3D'
    userEmail = 'kashyappadh@gmail.com'
    userPassword = ''
    browser = 'Firefox'

    def varReturnFunc(self):
        return self.__class__.baseUrl,self.__class__.userEmail,self.__class__.userPassword,self.__class__.browser