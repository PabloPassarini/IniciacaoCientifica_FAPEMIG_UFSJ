import csv, os, math,sys
from haversine import haversine, Unit


os.system('cls') # Limpando o terminal


def get_data(diretorio): #Função para a aquisição e tratamento dos dados
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for line in reader:
            aux.append(line) #Cada linha do arquivo é uma lista, então se colocarmos essa lista em outra lista, teremos uma matriz, nesse caso a matriz se chama aux
    
    del aux[len(aux)-1]  #Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
    del aux[0:11]        #Remove o cabeçalho do arquivo .csv
    
    for i in range(len(aux)):   
        #Removendo os caracteres desenecessários
        aux[i] = str(aux[i]).strip('[')     
        aux[i] = str(aux[i]).strip(']')
        aux[i] = str(aux[i]).strip("'")
        aux[i] = str(aux[i]).split(';')

        del aux[i][9] #Remove a ultima coluna, pois ela fica vazia, ('')
   
        #Remove as outras colunas, deixando somente a de data, precipitação, temperatura max e temperatura min

        del aux[i][1:3]
        del aux[i][3]
        del aux[i][4:6]

    real = list() #Lista/Matriz final

    #Removendo todas as linhas que possuem o valor null
    for i in range(len(aux)):
        condicao = 0
        for j in range(1,4):
            if aux[i][j] == 'null':
                condicao = 1
        
        if condicao == 0:
            real.append(aux[i])

    
    for i in range(len(real)): #Separando o dia, mes e ano da string
        aux.clear()
        for j in range(4):
            aux.append(real[i][j])
        data = aux[0]
        data = str(data).split('-')
        #print(data)
        real[i].insert(0, int(data[0]))
        real[i].insert(1, int(data[1]))
        real[i].insert(2, int(data[2]))
        del real[i][3]

    return real #Retorna a lista com os dados tratados, onde na lista em cada linha temos: [ano, mes, dia, precipitação, temperatura max, temperatura min]

def converte_coord(dado):
    dado = list(math.modf(dado))
    grau = int(dado[1])

    resto = dado[0]*60
    if resto < 0:
        resto = resto * (-1)
    
    resto = list(math.modf(resto))
    minuto = int(resto[1])
    segundos = round(resto[0]*60,4)

    return str(grau) + "° " + str(minuto) + "' " + str(segundos) + '" '

def get_coordinates(diretorio): #Função para obter as coordenadas de cada cidade
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for i in reader:
            aux.append(i)
        
    #Tratamento de dados
    del aux[10:]

    estacao = str(aux[0]).split(':')
    estacao = estacao[1].strip(']')
    estacao = (estacao.strip("'")).strip()

    latitude = str(aux[2]).split(':')
    latitude = latitude[1].strip(']')
    latitude = (latitude.strip("'")).strip()

    longitude = str(aux[3]).split(':')
    longitude = longitude[1].strip(']')
    longitude = (longitude.strip("'")).strip()

    altitude = str(aux[4]).split(':')
    altitude = altitude[1].strip(']')
    altitude = (altitude.strip("'")).strip()
    '''
    latitude = converte_coord(float(latitude))
    longitude = converte_coord(float(longitude))   
    '''
    aux.clear()
    aux.append(estacao)
    aux.append(latitude)
    aux.append(longitude)
    aux.append(altitude)

 
    return aux #Retorna um 'vetor' com os dados: [nome da estação, latitude, longitude, altitude]

def normaliza_dados(lista): #Função que retorna a matriz com os dados normalizados
    max_min = list()
    aux1 = list()
    for i in range(15): #Colocando os min e os max de cada coluna da lista tratada (anteriormente) em uma outra lista, fica assim: [ano min, ano max, mes min, mes max, precipitação min, precipitação max, temp max min, temp max max, temp min min, temp min max]
        aux1.clear()
        for j in range(len(lista)):
            aux1.append(float(lista[j][i]))
        max_min.append(min(aux1))
        max_min.append(max(aux1))  
    
    dadosn = list()
    #arq_teste = open("teste.txt", "w") Um arquivo só para manter os dados normalizados guardado
    for i in range(len(lista)):
        aux1.clear()
        for j in range(15):
            if j == 0: #Ano
                menor = max_min[0]
                maior = max_min[1]
            elif j == 1: #Mes
                menor = max_min[2]
                maior = max_min[3]
            elif j == 2: #Dia
                menor = max_min[4]
                maior = max_min[5]
            elif j == 3: #Precipitação
                menor = max_min[6]
                maior = max_min[7]
            elif j == 4: #Temperatura max
                menor = max_min[8]
                maior = max_min[9]
            elif j == 5: #Temperatura min
                menor = max_min[10]
                maior = max_min[11]
            elif j == 6: #Precipitação
                menor = max_min[12]
                maior = max_min[13]
            elif j == 7: #Temperatura max
                menor = max_min[14]
                maior = max_min[15]
            elif j == 8: #Temperatura min
                menor = max_min[16]
                maior = max_min[17]
            elif j == 9: #Precipitação
                menor = max_min[18]
                maior = max_min[19]
            elif j == 10: #Temperatura max
                menor = max_min[20]
                maior = max_min[21]
            elif j == 11: #Temperatura min
                menor = max_min[22]
                maior = max_min[23]
            elif j == 12: #Precipitação
                menor = max_min[24]
                maior = max_min[25]
            elif j == 13: #Temperatura max
                menor = max_min[26]
                maior = max_min[27]
            elif j == 14: #Temperatura min
                menor = max_min[28]
                maior = max_min[29]
            

            dado = ((float(lista[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
            
            aux1.append(dado)
        dadosn.append(aux1)
        #arq_teste.write(str(aux1[:])+"\n")
    return dadosn

def haversine_calc(a,b):
    tupla_1 = (float(a[1]), float(a[2]))
    tupla_2 = (float(b[1]), float(b[2]))

    return round(haversine(tupla_1, tupla_2, Unit.KILOMETERS), 4) #Retorna a distancia entre as duas cidades em Km, com 4 casas decimais

def dados_comum(cid1,cid2,cid3,cid4):
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
    arq = open(r'E:\IC\Códigos\analise.csv', 'w')
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
                        
                                    cond1 = 1
                                    break
                                                
                    if (cond1 == 1):
                        break
                        
            if(cond1 == 1):
                break
    return final


target = r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv'
neighorA = r'E:\IC\Dados\TriangulacaoBH\FLORESTAL.csv'
neighorB = r'E:\IC\Dados\TriangulacaoBH\IBIRITE.csv'
neighorC = r'E:\IC\Dados\TriangulacaoBH\SETELAGOAS.csv'

"""  ->Obtendo dados de cada cidade<-  """
targetData = get_data(target)
neighorAData = get_data(neighorA)
neighorBData = get_data(neighorB)
neighorCData = get_data(neighorC)

"""  ->Obtendo coordenadas de cada cidade<-  """
coord_target = get_coordinates(target)
coord_neighorA = get_coordinates(neighorA)
coord_neighorB = get_coordinates(neighorB)
coord_neighorC = get_coordinates(neighorC)

#print(normaliza_dados(targetData))

""""  ->Calculando a distancia entre as cidades<-  """
d1 = haversine_calc(coord_target, coord_neighorA) #Para a maior compreensão coloquei cada distancia em uma variavel, podia colocar direto na tupla 'd' (3 linhas a frente)
d2 = haversine_calc(coord_target, coord_neighorB)
d3 = haversine_calc(coord_target, coord_neighorC)


"""  ->Colocando a distancias entre cada cidade em uma tupla, e a altitude de cada uma em outra tupla<-  """
d = (d1, d2, d3) #Vetor com as distancias (Km) entre a cidade alvo e as 3 cidades vizinhas
h = (float(coord_target[3]), float(coord_neighorA[3]), float(coord_neighorB[3]), float(coord_neighorC[3])) #Alvo, vizinhaA, vizinhaB, vizinhaC


"""  ->Normalizando dados<-  """
comon_data = dados_comum(targetData, neighorAData, neighorBData, neighorCData)
datan = normaliza_dados(comon_data)

