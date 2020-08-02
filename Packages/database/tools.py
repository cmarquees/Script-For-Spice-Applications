
import csv
import time
import subprocess

def spiceProcess (cir, BIN):
    command = 'start ngspice ' + cir
    p = subprocess.Popen(command, shell= True, cwd= BIN)
    while p.poll() is None:
	    time.sleep(5)

def adjustFile_NGSPICE (file_path):
    adjustTxtList = []
    
    with open(file_path, newline='') as csvfile:
        txt = csv.reader(csvfile, delimiter=' ')
        for line in txt:
            nColumn = len(line)-1
            mColumn = 0
            f = False
            while (f == False):
                if(line[nColumn - mColumn] == ''):
                    line.pop(nColumn - mColumn)
                mColumn += 1
                if (nColumn < mColumn):
                    f = True
            adjustTxtList.append(line)

    return adjustTxtList

def get_bitflip(file_result, limTOP, limBOT, vdd, current, type):
    with open(file_result, 'r') as arq:
        vnode = arq.readline()
    if(current == limBOT or current == limTOP):
        return True, limTOP, limBOT

    elif(type == '0'):
        if(float(vnode) > (vdd/2)):
            limTOP = current
            return False, limTOP, limBOT

        else:
            limBOT = current
            return False, limTOP, limBOT

    elif (type == '1'):
        if(float(vnode) < (vdd/2)):
            limTOP = current
            return False, limTOP, limBOT
            
        else:
            limBOT = current
            return False, limTOP, limBOT

def getAxes (file_result, flag, wsnm):
    eixoX  = []
    eixoY  = []

    curves = adjustFile_NGSPICE(file_result)
    if(wsnm == False):
        if (flag == True):
            for line in curves:
                x = line[3]
                y = line[1]
                eixoX.append(float(x))
                eixoY.append(float(y))
        else:
            for line in curves:
                x = line[1]
                y = line[3]
                eixoX.append(float(y))
                eixoY.append(float(x))
    else:
        if (flag == True):
            for line in curves:
                x = line[1]
                y = line[3]
                eixoX.append(float(x))
                eixoY.append(float(y))
        else:
            for line in curves:
                x = line[3]
                y = line[1]
                eixoX.append(float(x))
                eixoY.append(float(y))

    return eixoX, eixoY

def store(list, storagePath, id):
    with open(storagePath + '/out.txt', 'w') as arq:
        if (id == 1):
            texto = "Tempos de atraso da Célula : "
            texto = texto + "\nEscrita do 0: "
            texto = texto + str(list[0])
            texto = texto + "\nEscrita do 1: "
            texto = texto + str(list[2])
            texto = texto + "\nLeitura do 0: "
            texto = texto + str(list[1])
            texto = texto + "\nLeitura do 1: "
            texto = texto + str(list[3])
            arq.writelines(texto)

        elif (id == 2):
            texto = "Tôlerancia a ruido da Célula : "
            texto = texto + "\nHSNM: "
            texto = texto + str(list[0])
            texto = texto + "\nRSNM: "
            texto = texto + str(list[1])
            texto = texto + "\nWSNM: "
            texto = texto + str(list[2])
            arq.writelines(texto)

        elif (id == 3):
            texto = "Robustes a radiação da Célula : \n"
            for line in list:
                texto += str(line) + '\n'
            arq.writelines(texto)