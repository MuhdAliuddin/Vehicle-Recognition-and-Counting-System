class Model:

    def __init__(self):

        self.fileName = None
        self.fileContent = ""

    def isValid(self, fileName):

        '''
        Checks if file input is valid
        '''

        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, fileName):

        '''
        Sets name of input video
        '''

        if self.isValid(fileName):
            self.fileName = fileName
        else:
            self.fileContents = ""
            self.fileName = ""

    def getFileName(self):
        
        '''
        Gets name of input video
        '''
        
        return self.fileName

        
