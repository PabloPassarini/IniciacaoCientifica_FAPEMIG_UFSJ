import csv, os
import subprocess
import _thread
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
    
    
    def get_data_trada(self): #! Funçao para retornar os dados tratados
        diretorio = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
       
        temp = [str(self.download) + "/alvo_limpa.txt", str(self.download) + "/vizinhaA_limpa.txt", str(self.download) + "/vizinhaB_limpa.txt", str(self.download) + "/vizinhaC_limpa.txt"]
        cont = 0
        comum_alvo = comum_vizA = comum_vizB = comum_vizC = list()

        for dir in diretorio:
            aux = list()
            with open(dir) as arq: #* Abrindo os arquivos .csv e armazenando numa lista
                reader = csv.reader(arq)
                for line in reader:
                    aux.append(line)
        
            del aux[len(aux)-1]      #? Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
            del aux[0:11]            #? Remove o cabeçalho do arquivo .csv
            
            for i in range(len(aux)): #* removendo caracteres e colunas desnecessários
                aux[i] = str(aux[i]).strip('[')     
                aux[i] = str(aux[i]).strip(']')
                aux[i] = str(aux[i]).strip("'")
                aux[i] = str(aux[i]).split(';')

                del aux[i][9] #* Removendo a ultima coluna, que está vazia '' 
                #* Deixando apenas as colunas de data, precipitação, temp max e temp min
                del aux[i][1:3]
                del aux[i][3]
                del aux[i][4:6]

            final = list()  #* Lista final 

            for i in range(len(aux)): #* Removendo todas as linhas que possuem o valor null em seu parametros
                condicao = 0
                for j in range(1,4):
                    if aux[i][j] == 'null':
                        condicao = 1

                if condicao == 0:
                    final.append(aux[i])    


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
            for i in final:
                if cont == 0:
                    comum_alvo.append(i)
                elif cont == 1:
                    comum_vizA.append(i)
                elif cont == 2:
                    comum_vizB.append(i)
                else:
                    comum_vizC.append(i)

                i = str(i).strip("[")
                i = str(i).strip("]")
                new_arq.write(str(i)+"\n")
            new_arq.close()
            cont += 1
        self.dadosc()
        
        

    def dadosc(self):
       subprocess.call(r'E:\IC\Interface_Grafica\codes\dadosc.py', shell=True)
       
    def retorna_arq(self, op):
        if op == 'Cidade alvo':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif op == 'Vizinha A':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif op == 'Vizinha B':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif op == 'Vizinha C':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'
        elif op == 'Dados comum':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\dadoscomum.csv'
        

        
        lista = list()
        arq = open(di) 
        for i in arq:
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
        if op == 'Cidade alvo':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif op == 'Vizinha A':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif op == 'Vizinha B':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif op == 'Vizinha C':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'
        elif op == 'Dados comum':
            di = r'E:\IC\Interface_Grafica\Dados_verificacao\dadoscomum.csv'
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
        arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\buff.txt')
        a = arq.readline()
        a = a.split()
        ut = int(a[0])
        Tar = int(a[1])
        vA = int(a[2])
        vB = int(a[3])
        vC = int(a[4])
        arq.close()
        return ut, Tar,vA, vB, vC