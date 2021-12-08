arq = open('E:\IC\locais_salvos.txt', 'r')
a = arq.read()
arq.close()


def get_dados(dir):
    arquivo = open(dir)
    resultado = list()
    for i in arquivo:
        resultado.append(i.strip())

    return resultado


alvo = get_dados(a + "/alvo_limpa.txt")
vizinhaA = get_dados(a + "/vizinhaA_limpa.txt")
vizinhaB = get_dados(a + "/viizinhaB_limpa.txt")
vizinhaC = get_dados(a + "/vizinhaC_limpa.txt")






for i in alvo:
    print(i)