from packages.database.files import *
from packages.database.tools import *

class Simulation:
    def __init__ ( self, preset):
        self.tech  = preset[0]
        self.node  = preset[1]
        self.model = preset[2]
        self.cell  = preset[3]
        self.sim   = preset[4]
        self.env   = preset[5]
        self.evt   = preset[6]
        self.addrs = FilesPath()


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

    def build (self):
        circuitAddress = self.addrs.PATH   + "/Circuits/Temp/tempCircuit.cir"
        resultAddress  = self.addrs.PATH   + "/Results/" + self.tech + '/'+ self.node + '_' + self.model + '/' + self.cell + '/' + self.sim
        if(self.evt == "OAM"):
            controlAddress  = self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/Cells/' + self.cell + '/' + self.sim + '_OAM.cir'
            selectAddress   = self.addrs.PATH + '/Circuits/Enviroments/select_OAM.cir'
        else:
            controlAddress  = self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/Cells/' + self.cell + '/' + self.sim + '.cir'
            selectAddress   = self.addrs.PATH + '/Circuits/Enviroments/select.cir'

        if (self.sim == "Delay"):
            cellAddress  = self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/Cells/' + self.cell + '/' + self.cell + '_Block.cir'
            if(self.evt == "C2"):
                selectAddress    = self.addrs.PATH + '/Circuits/Enviroments/select_c2.cir'
        elif (self.sim == "Noise"):
            cellAddress    = self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/Cells/' + self.cell + '/' + self.cell + '_Cell.cir'
        elif (self.sim == 'Radiation'):
            cellAddress      = self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/Cells/' + self.cell + '/' + self.cell + '_Block.cir'
            controlAddress  += '\n.include ' +  self.addrs.PATH + '/Circuits/Enviroments/' + self.sim + '/current_pulse.cir'
            if (self.env[4] == 'H'):
                resultAddress += '/Hold/' + self.evt
            elif (self.env[4] == 'R'):
                resultAddress += '/Read/' + self.evt
            elif (self.env[4] == 'W'):
                resultAddress += '/Write/' + self.evt


        with open(circuitAddress, 'w') as arq:
            inc =  '\n.include ' + self.addrs.PATH + '/Circuits/Files/' + self.tech + '/Essentials.cir'
            inc += '\n.include ' + self.addrs.PATH + '/Circuits/Files/' + self.tech + '/'+ self.node + '_' + self.model + '/'+ self.node + '_' + self.model +'.pm'
            inc += '\n.include ' + self.addrs.PATH + '/Circuits/Enviroments/' + self.sim + '/' + self.env
            inc += '\n.include ' + cellAddress
            inc += '\n.include ' + controlAddress
            inc += '\n.include ' + selectAddress
            inc += '\n\n '
            arq.writelines(inc)
            
        return circuitAddress, resultAddress

    def run (self):
        circuit, result = self.build()
        spiceProcess(circuit, self.addrs.BIN)
        return result