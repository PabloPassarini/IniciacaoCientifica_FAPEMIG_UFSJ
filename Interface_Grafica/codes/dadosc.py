from win10toast import ToastNotifier
def retorna_lista(diretorio):
    lista = list()
    arq = open(diretorio) 
    t = 0
    for i in arq:
        
        i = i.strip()
        i = i.replace("'",'')
        i = i.replace(" ",'')
        i = i.split(',')    
        lista.append(i)
        t += 1
    return lista, t

def dados_comum(cid1,cid2,cid3,cid4, t1, t2, t3, t4):
    ano_ini = max([cid1[0][0], cid2[0][0], cid3[0][0], cid4[0][0]])
    fim = min(len(cid1), len(cid2), len(cid3), len(cid4))
    
    for i in range(len(cid1)):
        if ano_ini == cid1[i][0]:
            ind1 = i
            break
    for i in range(len(cid2)):
        if ano_ini == cid2[i][0]:
            ind2 = i
            break
    for i in range(len(cid3)):
        if ano_ini == cid3[i][0]:
            ind3 = i
            break
    for i in range(len(cid4)):
        if ano_ini == cid4[i][0]:
            ind4 = i
            break

    final = list()
    aux = list()
    arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\dadoscomum.csv', 'w')
    arq_b = open(r'E:\IC\Interface_Grafica\Dados_verificacao\buff.txt', 'w')
    total = 0
    desc_a = desc_b = desc_c = 0
    for i in range(fim):
        ano1 = cid1[ind1+i][0]
        mes1 = cid1[ind1+i][1]
        dia1 = cid1[ind1+i][2]
        cond1 = 0
        for j in range(fim):
            ano2 = cid2[ind2+j][0]
            mes2 = cid2[ind2+j][1]
            dia2 = cid2[ind2+j][2]

            if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
                for k in range(fim):
                    ano3 = cid3[ind3+k][0]
                    mes3 = cid3[ind3+k][1]
                    dia3 = cid3[ind3+k][2] 
                    if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                            for z in range(fim):
                                ano4 = cid4[ind4+z][0]
                                mes4 = cid4[ind4+z][1]
                                dia4 = cid4[ind4+z][2]
                                if (ano3 == ano4) and (mes3 == mes4) and (dia3 == dia4):
                                    aux.clear()
                                    
                                    """  -> Adicionando os dados numa lista <-  """
                                    buff = ''   
                                    buff = str(ano1) + " " + str(mes1) + " " + str(dia1) + " " + cid1[ind1+i][3] + " " + cid1[ind1+i][4] + " " + cid1[ind1+i][5] + " " + cid2[ind2+j][3] + " " + cid2[ind2+j][4] + " " + cid2[ind2+j][5] + " " + cid3[ind3+k][3] + " " + cid3[ind3+k][4] + " " + cid3[ind3+k][5] + " " + cid4[ind4+z][3] + " " + cid4[ind4+z][4] + " " + cid4[ind4+z][5]  
                                    buff = str(buff).split()
                                    final.append(buff)
                                    
                                    """  -> Adicinando os dados num arquivo .csv <-  """
                                    buff = ''
                                    buff = str(ano1) + ";" + str(mes1) + ";" + str(dia1) + ";" + cid1[ind1+i][3] + ";" + cid1[ind1+i][4] + ";" + cid1[ind1+i][5] + ";" + cid2[ind2+j][3] + ";" + cid2[ind2+j][4] + ";" + cid2[ind2+j][5] + ";" + cid3[ind3+k][3] + ";" + cid3[ind3+k][4] + ";" + cid3[ind3+k][5] + ";" + cid4[ind4+z][3] + ";" + cid4[ind4+z][4] + ";" + cid4[ind4+z][5] + ";\n"
                                    arq.write(buff)
                                    total += 1
                                    cond1 = 1
                                    break
                                
                                  
                              
                    if (cond1 == 1):
                        break
              
            if(cond1 == 1):
                break
    arq_b.write(str(total) + " " + str(t1) + " " + str(t2) + " " + str(t3) + " " + str(t4))
    arq.close()
    arq_b.close()
    return final

alvo, talvo = retorna_lista(r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt')
vizinhaA, tA = retorna_lista(r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt')
vizinhaB, tB = retorna_lista(r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt')
vizinhaC, tC = retorna_lista(r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt')

dados_comum(alvo, vizinhaA, vizinhaB, vizinhaC, talvo, tA, tB, tC)
toast = ToastNotifier()
toast.show_toast("Algoritmo 1", "A execução do algoritmo1.py terminou", duration=30)

