
import csv, os
from encodings import utf_8
import re
from sunau import AUDIO_FILE_ENCODING_LINEAR_32
from win10toast import ToastNotifier


class Tratamento:
    global alvo
    global vizinhaA
    global vizinhaB
    global vizinhaC
    global download
    alvo = vizinhaA = vizinhaB = vizinhaC = download = ''
    def __init__(self):
        self.alvo = alvo
        self.vizinhaA = vizinhaA
        self.vizinhaB = vizinhaB
        self.vizinhaC = vizinhaC
        self.download = download
        
        
    # def __init__(self, alvo, vizinhaA, vizinhaB, vizinhaC, download):
    def procura_colunas(self, a, b):

        est = (str(b).split(' '))[2]
        est = est.strip("]")
        est = est.strip("'")
        

        if est[0] != 'A':
            coluna_prec = 3
            coluna_tmax = 4
            coluna_tmin = 6    
        else:
            coluna_prec = 1
            coluna_tmax = 4
            coluna_tmin = 6
            
        
        return coluna_prec, coluna_tmax, coluna_tmin
    def get_data_trada(self): #! Funçao para retornar os dados tratados
        diretorio = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
       
        temp = [str(self.download) + "/alvo_limpa.txt", str(self.download) + "/vizinhaA_limpa.txt", str(self.download) + "/vizinhaB_limpa.txt", str(self.download) + "/vizinhaC_limpa.txt"]
        
        arq1 = open("end.txt", "w")
        
        arq1.write(str(self.download) + "/alvo_limpa.txt\n" + str(self.download) + "/vizinhaA_limpa.txt\n" + str(self.download) + "/vizinhaB_limpa.txt\n" + str(self.download) + "/vizinhaC_limpa.txt\n" + str(self.download) + '/dadoscomum.csv\n' + str(self.download) + '/buff.txt\n' + str(self.download) + '/Coordenadas.txt\n')
        arq1.close()
        
        '''arq1 = open("end.txt", "w")
        arq1.write(str(self.download) + "/alvo_limpa.txt\n" + str(self.download) + "/vizinhaA_limpa.txt\n" + str(self.download) + "/vizinhaB_limpa.txt\n" + str(self.download) + "/vizinhaC_limpa.txt")
        arq1.close()'''
        cont = 0
        comum_alvo = comum_vizA = comum_vizB = comum_vizC = list()

        for dir in diretorio:
            aux = list()
            with open(dir) as arq: #* Abrindo os arquivos .csv e armazenando numa lista
                reader = csv.reader(arq, delimiter=';')
                for line in reader:
                    aux.append(line)
            del aux[10][len(aux[10])-1]

            cp, ctmax, ctmin = self.procura_colunas(aux[10], aux[1])

            del aux[len(aux)-1]      #? Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
            del aux[0:11]            #? Remove o cabeçalho do arquivo .csv

            colunas = [cp, ctmax, ctmin]
            
            buff = list()
            
            for i in range(len(aux)):
                buff2 = list()
                buff2.append(aux[i][0])
                for j in colunas:
                    buff2.append(aux[i][j])
                   
                buff.append(buff2)
            
            
                
            final = list()  #* Lista final 

            for i in range(len(buff)): #* Removendo todas as linhas que possuem o valor null em seu parametros
                condicao = 0
                for j in range(1,4):
                    if buff[i][j] == 'null' or buff[i][j] == '':
                        condicao = 1

                if condicao == 0:
                    final.append(buff[i])
                       

            
            for i in range(len(final)): #* Passando a data de AAAA-MM-DD para AAAA, MM, DD
                aux.clear()
                
                for j in range(4):
                    aux.append(final[i][j])
                
                data = aux[0]
                data = str(data).split('-')

                final[i].insert(0, int(data[0]))
                final[i].insert(1, int(data[1]))
                final[i].insert(2, int(data[2]))
        
                del final[i][3]
           
            new_arq = open(temp[cont], 'w')    #TODO: Salvando os dados em arquivos .txt
            teste = list()
            for i in final:
                aux = list()
                for j in range(len(i)):
                    aux.append(str(i[j]).replace(',', '.'))
                teste.append(aux)
            for i in teste:
                if cont == 0:
                    comum_alvo.append(str(i).replace(' ', ''))
                elif cont == 1:
                    comum_vizA.append(str(i).replace(' ', ''))
                elif cont == 2:
                    comum_vizB.append(str(i).replace(' ', ''))
                else:
                    comum_vizC.append(str(i).replace(' ', ''))

                i = str(i).strip("[")
                i = str(i).strip("]")
                i = i.replace(' ', '')
                
                
                new_arq.write(str(i)+"\n")
            new_arq.close()
            cont += 1
        self.get_coordinates()
        
        self.dadosc2()
        
    def dadosc(self):
        #subprocess.call(r'E:\IC\Interface_Grafica\codes\dadosc.py', shell=True)
        cid1, t1 = self.prepara_dadosc(str(self.download) + "/alvo_limpa.txt")
        cid2, t2 = self.prepara_dadosc(str(self.download) + "/vizinhaA_limpa.txt")
        cid3, t3 = self.prepara_dadosc(str(self.download) + "/vizinhaB_limpa.txt")
        cid4, t4 = self.prepara_dadosc(str(self.download) + "/vizinhaC_limpa.txt")
        
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
        '''
        arq1 = open('end.txt', 'a')
        arq1.write('\n' + str(self.download) + '/dadoscomum.csv\n' + str(self.download) + '/buff.txt\n' + '/Coordenadas.txt\n')
        arq1.close()
        '''
        arq = open(str(self.download) + '/dadoscomum.txt', 'w')
        arq_b = open(str(self.download) + '/buff.txt', 'w')
        total = 0
        ind1 = ind2 = ind3 = ind4 = 0
        
        for i in range(fim):
            
            ano1 = int(cid1[ind1+i][0])
            mes1 = int(cid1[ind1+i][1])
            dia1 = int(cid1[ind1+i][2])
            cond1 = 0
            for j in range(fim):
                ano2 = int(cid2[ind2+j][0])
                mes2 = int(cid2[ind2+j][1])
                dia2 = int(cid2[ind2+j][2])
                #print("{} {} {}  ||  {} {} {}".format(ano1, mes1, dia1, ano2, mes2, dia2))
                
                if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
                    
                    for k in range(fim):
                        ano3 = int(cid3[ind3+k][0])
                        mes3 = int(cid3[ind3+k][1])
                        dia3 = int(cid3[ind3+k][2]) 
                        
                        if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                                
                                
                                for z in range(fim):
                                    ano4 = int(cid4[ind4+z][0])
                                    mes4 = int(cid4[ind4+z][1])
                                    dia4 = int(cid4[ind4+z][2])
                                    
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
        
    def dadosc2(self):
        alv, t1 = self.prepara_dadosc(str(self.download) + "/alvo_limpa.txt")
        vizA, t2 = self.prepara_dadosc(str(self.download) + "/vizinhaA_limpa.txt")
        vizB, t3 = self.prepara_dadosc(str(self.download) + "/vizinhaB_limpa.txt")
        vizC, t4 = self.prepara_dadosc(str(self.download) + "/vizinhaC_limpa.txt")
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
        arq = open(str(self.download) + '/dadoscomum.csv', 'w')
        arq_b = open(str(self.download) + '/buff.txt', 'w')
        comum =0
        for i in range(ind1, len(alv)):
            try:
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
                                        #print("\nAlvo:{}\nVizinhaA:{}\nVizinhaB:{}\nVizinhaC:{}\n".format(type(alv[i]),type(vizA[j]), type(vizB[k]), type(vizC[l])))
                                        t_alv = str(alv[i]).strip('[')
                                        t_alv = t_alv.strip(']')
                                        t_alv = t_alv.replace(' ', '')
                                        
                                        del vizA[j][:3]
                                        t_vizA = str(vizA[j]).strip('[')
                                        t_vizA = t_vizA.strip(']')
                                        t_vizA = t_vizA.replace(' ', '')
                                        
                                        del vizB[k][:3]
                                        t_vizB = str(vizB[k]).strip('[')
                                        t_vizB = t_vizB.strip(']')
                                        t_vizB = t_vizB.replace(' ', '')
                                        
                                        del vizC[l][:3]
                                        t_vizC = str(vizC[l]).strip('[')
                                        t_vizC = t_vizC.strip(']')
                                        t_vizC = t_vizC.replace(' ', '')

                                        texto = t_alv + ',' + t_vizA + ',' + t_vizB + ',' + t_vizC
                                        texto = texto.replace(',', ';')
                                        
                                        #texto  = str(ano1) + ";" + str(mes1) + ";" + str(dia1) + ";" + alv[ind1+i][3] + ";" + alv[ind1+i][4] + ";" + alv[ind1+i][5] + ";" + vizA[ind2+j][3] + ";" + vizA[ind2+j][4] + ";" + vizA[ind2+j][5] + ";" + vizB[ind3+k][3] + ";" + vizB[ind3+k][4] + ";" + vizB[ind3+k][5] + ";" + vizC[ind4+l][3] + ";" + vizC[ind4+l][4] + ";" + vizC[ind4+l][5] + ";\n"                           
                                        
                                        arq.write(texto + ';\n')
                                        comum += 1    
            except IndexError:
                pass
        arq_b.write(str(comum) + " " + str(t1) + " " + str(t2) + " " + str(t3) + " " + str(t4))
        arq.close()
        arq_b.close()

    def prepara_dadosc(self, dir):
        arq = open(dir)
        lista = list()

        t=0
        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',')    
            lista.append(i)
            
            t += 1
        
        return lista, t


    def retorna_arq(self, op):
        arq = open('end.txt') 
        a = arq.readlines()
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            
        

        
        lista = list()
        
        arq = open(di)
        
        for i in arq:
            
            i = i.replace('\n', '')
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            
            if op == 'Dados comum':
                i = i.split(';')
                del i[len(i)-1]
                
            else:
                i = i.split(',')  
            lista.append(i)
        arq.close()
        
        return lista
    
    def get_range(self, op):
        controle = 0
        arq = open('end.txt') 
        a = arq.readlines()
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            controle = 1
            
        arq = open(di)
        aux = list()

        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            if controle == 1:
                i = i.split(';')
                del i[len(i)-1]
            else:
                i = i.split(',')
            aux.append(int(i[0]))
        arq.close()
        
        anos = list()
        
        buff = aux[0]
    
        anos.append(buff)
        
        for i in range(1,len(aux)): 
            try:
                if aux[i-1] != aux[i]:
                    buff = aux[i]
                    anos.append(buff)
            except IndexError:
                pass
        return anos

    def get_qtd(self):
        arq = open('end.txt') 
        a = arq.readlines()
        arq = open(a[5].replace("\n", ''))
        
        a = arq.readline()
        a = a.split()
        ut = int(a[0])
        Tar = int(a[1])
        vA = int(a[2])
        vB = int(a[3])
        vC = int(a[4])
        arq.close()
        return ut, Tar,vA, vB, vC

    def normalizar_dados(self, mat):
        max_min = list()
        aux = list()
        t = len(mat[0])
        for i in range(t):
            aux.clear()
            for j in range(len(mat)):
                aux.append(mat[j][i])
            max_min.append(max(aux))
            max_min.append(min(aux))

        dadosn =list()
        
    
        for i in range(len(mat)):
            cont = 0
            buff = list()
            for j in range(t):
                if cont <= 36:
                    maior = max_min[cont]
                    menor = max_min[cont + 1]
                    dado = ((float(mat[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                    buff.append(dado)
                    cont = cont + 2
            dadosn.append(buff)
        
        
        return dadosn

    def get_coordinates(self): # ? Função para obter as coordenadas de cada cidade
        coordenadas = list()
        aux = list()
        arq1 = open('end.txt') 
        a = arq1.readlines()
        locais = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
        
        for i in locais:
            aux.clear()
            with open(i) as arq:
                reader = csv.reader(arq)
                for j in reader:
                    aux.append(j)
            arq.close()
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

            coordenadas.append(estacao)
            coordenadas.append(latitude)
            coordenadas.append(longitude)
            coordenadas.append(altitude)
        
        arq = open(a[6].replace("\n", ''), 'w')
        for i in coordenadas:
            arq.write(i)
            arq.write('\n')
        arq1.close() 
        arq.close()    
    
    def get_local_cord(self):
        arq = open('end.txt') 
        a = arq.readlines()
        aux = a[6].replace("\n", '')
        return aux

    def retorna_end(self, op):
        arq = open('end.txt') 
        a = arq.readlines()

        if op == 'Cidade alvo':
            return a[0].replace("\n", '')
        elif op == 'Vizinha A':
            return a[1].replace("\n", '')
        elif op == 'Vizinha B':
            return a[2].replace("\n", '')
        elif op == 'Vizinha C':
            return a[3].replace("\n", '')