from packages.business.simulation import *
from packages.business.meas import *

class Menu:
    def __init__ (self, userConfig):
        self.setup = userConfig
        self.temp  = Simulation(userConfig)

    def features(self):
        if(self.setup[4] == "Delay"):
            rAddress = self.temp.run()

            if ((self.setup[5] == "Validation_vdd.cir") or (self.setup[5] == "Validation_gnd.cir")):
                measDelay_Type1(self.temp.addrs.OUT, rAddress)

            elif (self.setup[5] == "Validation_rbl.cir"):
                measDelay_Type2(self.temp.addrs.OUT, rAddress)

        elif(self.setup[4] == "Noise"):
            output = self.temp.measNoise_Type1(self.circuit, self.setup[3],  outCircuit ,self.result)
            store(output, tempCircuit[1], 2)
        
        elif(self.setup[4] == 'Radiation'):
            if(self.setup[5][4] == 'H'):
                op = 'Hold'
            elif(self.setup[5][4] == 'R'):
                op = 'Read'
            elif(self.setup[5][4] == 'W'):
                op = 'Write'

            output = measLET_Type1(tempCircuit[0], self.setup[3],  outCircuit, op, self.setup[6])
            store(output, tempCircuit[1], 3)



                    self.circuit, self.result = self.temp.build()