from packages.database.tools import *


# DELAY #
def measDelay_Type1 (file_result, store_address):
    adjustedList = adjustFile_NGSPICE(file_result)

    time   = []
    out    = []
    vdd    = 0.7
    sense  = 0.035
    flag   = True
    write0 = False
    write1 = False
    read0  = False
    read1  = False

    for line in adjustedList:
        if(write0 == True):
            vnode = float(line[3])
            if(vnode <= (vdd*0.5)):
                out.append(float(line[0]) - time[0])
                write0 = False
        elif(write1 == True):
            vnode = float(line[3])
            if(vnode >= (vdd*0.5)):
                out.append(float(line[0]) - time[2])
                write1 = False
        elif(read0 == True):
            bl  = float(line[5])
            blb = float(line[7])
            diferenca = abs(blb-bl)
            if(diferenca > sense):
                out.append(float(line[0]) - time[1])
                read0 = False
        elif(read1 == True):
            bl  = float(line[5])
            blb = float(line[7])
            diferenca = abs(bl-blb)
            if(diferenca > sense):
                out.append(float(line[0]) - time[3])
                read1 = False
        elif (flag == True):
            wl_now = float(line[1])
            flag = False
        else:
            wl_ant  = wl_now
            wl_now  = float(line[1])
            if((wl_ant <= (vdd*0.5)) and (wl_now > (vdd*0.5))):
                time.append(float(line[0]))
                tam = len(time)
                if(tam == 1):
                    # Escrevendo 0
                    write0 = True
                elif(tam == 3):
                    # Escrevendo 1
                    write1 = True
                elif(tam == 2):
                    # Leitura 0
                    read0 = True
                elif(tam == 4):
                    # Leitura 1
                    read1 = True
    s

def measDelay_Type2 (file_result, store_address):
    adjustedList = adjustFile_NGSPICE(file_result)

    time   = []
    out    = []
    vdd   = 0.7
    sense = 0.035
    flag   = True
    write0 = False
    write1 = False
    read0  = False
    read1  = False

    for line in adjustedList:
        if(write0 == True):
            vnode = float(line[3])
            if(vnode <= (vdd*0.5)):
                out.append(float(line[0]) - time[0])
                write0 = False
        elif(write1 == True):
            vnode = float(line[3])
            if(vnode >= (vdd*0.5)):
                out.append(float(line[0]) - time[2])
                write1 = False
        elif(read0 == True):
            bl  = float(line[9])
            blb = float(line[11])
            diferenca = blb-bl
            if(diferenca > sense):
                out.append(float(line[0]) - time[1])
                read0 = False
        elif(read1 == True):
            bl  = float(line[9])
            blb = float(line[11])
            diferenca = bl-blb
            if(diferenca > sense):
                out.append(float(line[0]) - time[3])
                read1 = False
        elif (flag == True):
            wl_now = float(line[1])
            rwl_now = float(line[13])
            flag = False
        else:
            wl_ant  = wl_now
            rwl_ant = rwl_now
            wl_now  = float(line[1])
            rwl_now = float(line[13])
            if(((wl_ant <= (vdd*0.5)) and (wl_now > (vdd*0.5))) or (((rwl_ant <= (vdd*0.5)) and (rwl_now > (vdd*0.5))))):
                time.append(float(line[0]))
                tam = len(time)
                if(tam == 1):
                    # Escrevendo 0
                    write0 = True
                elif(tam == 3):
                    # Escrevendo 1
                    write1 = True
                elif(tam == 2):
                    # Leitura 0
                    read0 = True
                elif(tam == 4):
                    # Leitura 1
                    read1 = True
    print(out)
    return out

# NOISE #
def measNoise_Type1 (cir, cell, file_result, out_path):
    snm = PATH + '/Circuits/Enviroments/Noise/snm.cir'
    erro = 0.01
    out = []
   # Ambiente HSNM 
    if (cell == '6T'):    
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vrwl rwl gnd DC 0 \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC 0 \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)

    # Executa Simulação
    spiceProcess(cir)
    curveA = getAxes(file_result, True, False)
        
        
    # Ambiente HSNM b
    if(cell == '6T'):    
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vrwl rwl gnd DC 0 \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC 0 \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)

    # Executa Simulação
    spiceProcess(cir)
    curveB = getAxes(file_result, False, False)
    plot_out = out_path + '/HSNM.png'
    out.append(getSquare(curveA, curveB, erro, plot_out))

   # Ambiente RSNM 
    if(cell == '6T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vrwl rwl gnd DC supply \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC 0 \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)

    # Executa Simulação
    spiceProcess(cir)
    curveA = getAxes(file_result, True, False)

    # Ambiente RSNM b
    if(cell == '6T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC 0 \n'
        texto += 'Vrwl rwl gnd DC supply \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC 0 \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC supply \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)
        
    # Executa Simulação
    spiceProcess(cir)
    curveB = getAxes(file_result, False, False)

    plot_out = out_path + '/RSNM.png'
    out.append(getSquare(curveA, curveB, erro, plot_out))

   # Ambiente WSNM 
    if(cell == '6T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vrwl rwl gnd DC 0 \n'
        texto += 'Vvn q gnd DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vq q vn DC 0 \n'
        texto += 'Vq2 q2 vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)

    # Executa Simulação
    spiceProcess(cir)
    curveA = getAxes(file_result, True, True)

    # Ambiente HSNM b
    if(cell == '6T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == '8T' or cell == '9T'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vrwl rwl gnd DC 0 \n'
        texto += 'Vvn qb gnd DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'
        texto += 'Vrbl rbl gnd DC supply \n'

    elif (cell == '8TSER'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'

    elif (cell == 'DICE'):
        texto =  'Vvcell vcell gnd DC supply \n'
        texto += 'Vwl wl gnd DC supply \n'
        texto += 'Vvn vn gnd DC 0 \n'
        texto += 'Vqb qb vn DC 0 \n'
        texto += 'Vq2b q2b vn DC 0 \n'
        texto += 'Vbl bl gnd DC 0 \n'
        texto += 'Vblb bl_b gnd DC supply \n'
    

    # Atualiza o arquivo
    with open(snm, 'w') as arq:
        arq.writelines(texto)
        
    # Executa Simulação
    spiceProcess(cir)
    curveB = getAxes(file_result, False, True)

    plot_out = out_path + '/WSNM.png'
    out.append(getSquare(curveA, curveB, erro, plot_out))

    return out

# RADIATION #
def measLET_Type1 (cir, cell, file_result, mode, event):
    current_file = PATH + '/Circuits/Enviroments/Radiation/current_pulse.cir'
    current = 114
    vdd     = 0.7
    out     = []
    
    if (mode == 'Hold'):
        insert = '3.00n'
    elif (mode == 'Read'):
        insert = '2.60n'
    elif (mode == 'Write'):
        insert = '3.14n'
    
    if (event == 'SEU'):
        if (cell == '6T'):
            nodos = ['q', 'qb']
        elif (cell == 'DICE' or cell == '8TSER'):
            nodos = ['q', 'qb', 'q2', 'q2b']
        elif (cell == '8T' or cell == '9T'):
            nodos = ['q', 'qb']

    elif (event == 'SET'):
        nodos = ['bl_c1', 'bl_b_c1']

    elif (event == 'OAM'):
        if (cell == '6T'):
            nodos = ['q_2', 'qb_2', 'bl_c2', 'bl_b_c2']
        elif (cell == 'DICE' or cell == '8TSER'):
            nodos = ['q_2', 'qb_2', 'q2_2', 'q2b_2', 'bl_c2', 'bl_b_c2']
        elif (cell == '8T' or cell == '9T'):
            nodos = ['q_2', 'qb_2', 'bl_c2', 'bl_b_c2']

    for nodo in nodos:
       # Ambiente Nodo 010
        amb    = '010'
        stop   = False
        limTOP = 5000
        limBOT = 0 

        while (stop == False):     
            # Atualiza a corrente
            current = ((limTOP+limBOT)//2)

            # Seta ambiente 
            if(nodo.count("b") > 1 or (nodo.count("b") == 1 and nodo[0] != 'b')):
            #if((nodo[len(nodo)-1] == 'b') or (nodo[len(nodo)-3] == 'b') or (nodo[len(nodo)-4] == 'b')):
                with open(current_file, 'w') as arq:
                    texto =  'Vaux aux ' + nodo + ' DC 0 \n'
                    texto += "Iseu gnd aux EXP (0 " + str(current) + "u " + str(insert) + " 10p '10p+" + str(insert) + "' 200p)\n"
                    if (event == 'OAM'):
                        texto += 'Vbit bit gnd DC supply \n'
                    else:
                        if (mode == 'Write'): 
                            texto += 'Vbit bit gnd PWL 0n 0 2n 0 2.000001n supply 8n supply\n'
                        else:
                            texto += 'Vbit bit gnd DC supply \n'
                    arq.writelines(texto)
                
                # Executa Simulação
                spiceProcess(cir)

                # Verifica o efeito
                t = '1'
                stop, limTOP, limBOT = get_bitflip(file_result, limTOP, limBOT, vdd, current, t)
 
            else:
                with open(current_file, 'w') as arq:
                    texto =  'Vaux aux ' + nodo + ' DC 0 \n'
                    texto += "Iseu gnd aux EXP (0 " + str(current) + "u " + str(insert) + " 10p '10p+" + str(insert) + "' 200p)\n"
                    if (event == 'OAM'):
                        texto += 'Vbit bit gnd DC 0 \n'
                    else:
                        if (mode == 'Write'): 
                            texto += 'Vbit bit gnd PWL 0n supply 2n supply 2.000001n 0 8n 0\n'
                        else:
                            texto += 'Vbit bit gnd DC 0 \n'
                    arq.writelines(texto)

                # Executa Simulação
                spiceProcess(cir)

                # Verifica o efeito
                t = '0'
                stop, limTOP, limBOT = get_bitflip(file_result, limTOP, limBOT, vdd, current, t)
        
        #print(nodo + '  ' + str(current) + ' ' + t)
        out.append((nodo, current, amb))

       # Ambiente Nodo 101
        amb  = '101'
        stop = False
        limTOP = 5000
        limBOT = 0

        while (stop == False):
            # Atualiza a corrente
            current = ((limTOP+limBOT)//2)

            # Seta ambiente
            if(nodo.count("b") > 1 or (nodo.count("b") == 1 and nodo[0] != 'b')):
            #if((nodo[len(nodo)-1] == 'b') or (nodo[len(nodo)-3] == 'b') or (nodo[len(nodo)-4] == 'b')):
                with open(current_file, 'w') as arq:
                    texto =  'Vaux aux ' + nodo + ' DC 0 \n'
                    texto += "Iseu aux gnd EXP (0 " + str(current) + "u " + str(insert) + " 10p '10p+" + str(insert) + "' 200p)\n"
                    if (event == 'OAM'):
                        texto += 'Vbit bit gnd DC 0 \n'
                    else:
                        if (mode == 'Write'): 
                            texto += 'Vbit bit gnd PWL 0n supply 2n supply 2.000001n 0 8n 0\n'
                        else:
                            texto += 'Vbit bit gnd DC 0 \n'
                    arq.writelines(texto)

                # Executa Simulação
                spiceProcess(cir)

                # Verifica o efeito
                t = '0'
                stop, limTOP, limBOT = get_bitflip(file_result, limTOP, limBOT, vdd, current, t)

            else:
                with open(current_file, 'w') as arq:
                    texto =  'Vaux aux ' + nodo + ' DC 0 \n'
                    texto += "Iseu aux gnd EXP (0 " + str(current) + "u " + str(insert) + " 10p '10p+" + str(insert) + "' 200p)\n"
                    if (event == 'OAM'):
                        texto += 'Vbit bit gnd DC supply \n'
                    else:
                        if (mode == 'Write'): 
                            texto += 'Vbit bit gnd PWL 0n 0 2n 0 2.000001n supply 8n supply\n'
                        else:
                            texto += 'Vbit bit gnd DC supply \n'
                    
                    arq.writelines(texto)

                # Executa Simulação
                spiceProcess(cir)

                # Verifica o efeito
                t = '1'
                stop, limTOP, limBOT = get_bitflip(file_result, limTOP, limBOT, vdd, current, t)

        #print(nodo + '  ' + str(current) + ' ' + t)
        out.append((nodo, current, amb))

    return out
