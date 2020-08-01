from Packages.database import files

class Simulation:
    def __init__ ( self, preset):
        self.tech = preset[0]
        self.node = preset[1]
        self.model= preset[2]
        self.cell = preset[3]
        self.sim  = preset[4]
        self.env  = preset[5]
        self.evt  = preset[6] 


    def getTech (self):
        return self.tech

    def getNode (self):
        return self.node

    def getModel (self):
        return self.model

    def getCell (self):
        return self.cell

    def getSimu (self):
        return self.sim

    def getEnv (self):
        return self.env

    def getEvt (self):
        return self.evt

