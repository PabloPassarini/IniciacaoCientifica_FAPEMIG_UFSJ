import os
os.system('cls')

def retorna_arq(dir):
    arq = open(dir, 'r')
    lista = list()
    tam = 0
    for i in arq:
        i = i.strip()
        i = i.replace("'",'')
        i = i.replace(" ",'')
        i = i.split(',')
        lista.append(i)
        tam += 1
    
    arq.close()
    return lista, tam

alv, t1 = retorna_arq(r'E:/IC/Dados/NOVAS REGIOES/AMPA/dados/alvo_limpa.txt')
vizA, t2 = retorna_arq(r'E:/IC/Dados/NOVAS REGIOES/AMPA/dados/vizinhaA_limpa.txt')
vizB, t2 = retorna_arq(r'E:/IC/Dados/NOVAS REGIOES/AMPA/dados/vizinhaB_limpa.txt')
vizC, t2 = retorna_arq(r'E:/IC/Dados/NOVAS REGIOES/AMPA/dados/vizinhaC_limpa.txt')

print("{} {} {} {}".format(alv[0], vizA[0], vizB[0], vizC[0]))
comeca = max(alv[0][0], vizA[0][0], vizB[0][0], vizC[0][0])

ind1 = ind2 = ind3 = ind4 = 0
for i in range(len(alv)):
    if int(comeca )== int(alv[i][0]):
        ind1 = i
        break
for i in range(len(vizA)):
    if int(comeca)== int(vizA[i][0]):
        ind2 = i
        break
for i in range(len(vizA)):
    if int(comeca)== int(vizB[i][0]):
        ind3 = i
        break
for i in range(len(vizA)):
    if int(comeca)== int(vizC[i][0]):
        ind4 = i
        break
print("{} - {} | {} - {} | {} - {} | {} - {}".format(ind1, alv[ind1], ind2, vizA[ind2], ind3, vizB[ind3], ind4, vizC[ind4]))
comum = 0
arq = open(r'E:/IC/Dados/NOVAS REGIOES/AMPA/dados/dadoscomum.txt', 'w')
for i in range(ind1, len(alv)):
    
    ano1 = alv[i][0]
    mes1 = alv[i][1]
    dia1 = alv[i][2]
    for j in range(ind2, len(vizA)):
        ano2 = vizA[j][0]
        mes2 = vizA[j][1]
        dia2 = vizA[j][2]
        if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
            for k in range(ind3, len(vizB)):
                ano3 = vizB[k][0]
                mes3 = vizB[k][1]
                dia3 = vizB[k][2]
                if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                    for l in range(ind4, len(vizC)):
                        ano4 = vizC[l][0]
                        mes4 = vizC[l][1]
                        dia4 = vizC[l][2]
                        if (ano3 == ano4) and (mes3 == mes4) and (dia3 == dia4):
                            #print("\nAlvo:{}\nVizinhaA:{}\nVizinhaB:{}\nVizinhaC:{}\n".format(alv[i],vizA[j], vizB[k], vizC[l]))
                            texto = str(ano1) + ';' + str(mes1) + ';' + str(dia1) + ';' + str(alv[i][3]) + ';' + str(alv[i][4]) + ';' + str(alv[i][5]) + ';' + str(vizA[j][3]) + ';' + str(vizA[j][4]) + ';'  + str(vizB[j][5]) + ';\n'
                            arq.write(texto)
                            print(len(alv[i]))
                            comum += 1
arq.close()
print(comum)
