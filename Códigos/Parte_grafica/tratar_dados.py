import csv

class Data_trat:
    def __init__(self, alvo, vizinhaA, vizinhaB, vizinhaC, donwload):
        self.alvo = alvo
        self.vizinhaA = vizinhaA
        self.vizinhaB = vizinhaB
        self.vizinhaC = vizinhaC
        self.download = donwload
    
    def get_data_trada(self): #! Funçao para retornar os dados tratados
        diretorio = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
       
        temp = [str(self.download) + "/alvo_limpa.txt", str(self.download) + "/vizinhaA_limpa.txt", str(self.download) + "/vizinhaB_limpa.txt", str(self.download) + "/vizinhaC_limpa.txt"]
        cont = 0
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
                i = str(i).strip("[")
                i = str(i).strip("]")
                new_arq.write(str(i)+"\n")
            new_arq.close()
            cont += 1
'''
    def tratar(diretorio): #! Função para tratar os dados tratados
        aux = list()   

        with open(diretorio) as arq: #* Abrindo os arquivos .csv e armazenando numa lista
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

        for i in range(len(aux)): #! Removendo todas as linhas que possuem o valor null em seu parametros
            condicao = 0
            for j in range(1,4):
                if aux[i][j] == 'null':
                    condicao = 1

            if condicao == 0:
                final.append(aux[i])    


        for i in range(len(final)):
            aux.clear()
            for j in range(4):
                aux.append(final[i][j])
            data = aux[0]
            data = str(data).split('-')

            final[i].insert(0, int(data[0]))
            final[i].insert(1, int(data[1]))
            final[i].insert(2, int(data[2]))
            del final[i][3]
            
        return final

'''

