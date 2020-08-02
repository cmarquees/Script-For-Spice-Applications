class FilesPath:
    def __init__ (self, imput):
        self.PATH   = "C:/Users/Cleiton/Documents/Simulations"
        self.BIN    = "C:/Users/Cleiton/Documents/Simulations/Tools/NGSpice/bin"
        self.RESULT = "C:/Users/Cleiton/Documents/Simulations/Results"
        self.OUT    = self.BIN + "/Temp/" + imput[4] + "/" + imput[3] + "/out.txt"


    def getPath (self):
        return self.PATH

    def getBin (self):
        return self.BIN

    def getResult (self):
        return self.RESULT

    def getOut (self):
        return self.OUT