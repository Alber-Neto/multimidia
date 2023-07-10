import argparse 
import os 
import heapq
import collections

class Huff:

    def __init__(self,frequencia=0 , simbolo=None, esquerda=None, direita=None):
        self.simbolo = simbolo  
        self.frequencia = frequencia  
        self.esquerda = esquerda  
        self.direita = direita 
        self.digito = ""

    def __lt__(self, outro):
        return self.frequencia < outro.frequencia 

codigos = dict()

def calcular_codigos(no, valor=""):
    novovalor =valor + str(no.digito)

    if(no.esquerda):
        calcular_codigos(no.esquerda, novovalor)
    if(no.direita):
        calcular_codigos(no.direita, novovalor)

    if(not no.esquerda and not no.direita):
        codigos[no.simbolo] = novovalor
    
    return codigos

def Calcular_probabilidade(dados):
    simbolos = dict()
    for elementos in dados:
        if simbolos.get(elementos) == None:
            simbolos[elementos] = 1
        else: 
            simbolos[elementos] += 1     
    return simbolos

def saida_de_dados(dados, codificação):
    saida_codificada = []
    for c in dados:
        saida_codificada.append(codificação[c])
    string = ''.join([str(item) for item in saida_codificada])

    return string

def espaco_economizado(dados, codificação):
    antes=len(dados)
    depois=0
    simbolos=codificação.keys()
    for simbolo in simbolos:
        count=dados.count(simbolo)
        depois+= count * len(codificação[simbolo])
    return antes,depois

def huffman_compilar(dados):
    probabilidade_simbolos = Calcular_probabilidade(dados)
    simbolos = probabilidade_simbolos.keys()
    probailidades = probabilidade_simbolos.values()

    nos = []

    for simbolo in simbolos:
        nos.append(Huff(probabilidade_simbolos.get(simbolo),simbolo))

    while len(nos) > 1:
        nos = sorted(nos, key=lambda x: x.frequencia)
        direita= nos[0]
        esquerda = nos[1]
        direita.digito = 0
        esquerda.digito = 1

        novono = Huff(esquerda.frequencia+direita.frequencia, esquerda.simbolo+direita.simbolo,esquerda,direita)
        nos.remove(esquerda)
        nos.remove(direita)
        nos.append(novono)
    huffman_codificado = calcular_codigos(nos[0])
    huffman_codificado = dict(sorted(huffman_codificado.items(), key=lambda x: x[1]))
    saida=saida_de_dados(dados,huffman_codificado)
    bits = ""
    bits += saida
    bits += "0" * (8 - len(bits) % 8)
    bytes_ = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return bytes_

def huffman_descompilar(dados):
    probabilidade_simbolos = Calcular_probabilidade(dados)
    simbolos = probabilidade_simbolos.keys()
    probailidades = probabilidade_simbolos.values()

    nos = []

    for simbolo in simbolos:
        nos.append(Huff(probabilidade_simbolos.get(simbolo),simbolo))

    while len(nos) > 1:
        nos = sorted(nos, key=lambda x: x.frequencia)
        direita= nos[0]
        esquerda = nos[1]
        direita.digito = 0
        esquerda.digito = 1

        novono = Huff(esquerda.frequencia+direita.frequencia, esquerda.simbolo+direita.simbolo,esquerda,direita)
        nos.remove(esquerda)
        nos.remove(direita)
        nos.append(novono)
    huffman_codificado = calcular_codigos(nos[0])
    huffman_codificado = dict(sorted(huffman_codificado.items(), key=lambda x: x[1]))
    saida=saida_de_dados(dados,huffman_codificado)

    arvore_raiz = nos[0]
    dados_decodificado = huffman_codificado
    for x in dados:
        if x == '1':
            arvore_raiz=arvore_raiz.direita
        elif x == '0':
            arvore_raiz=arvore_raiz.esquerda
        try:
            if arvore_raiz.esquerda.simbolo == None and arvore_raiz.direita.simbolo == None:
                pass
        except AttributeError:
            dados_decodificado.append(arvore_raiz.simbolo)
            arvore_raiz=arvore_raiz
        texto = ''.join([str(item) for item in dados_decodificado])
        return texto

def ler_arquivo(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return data

def ler_arquivo_txt(filename):
    with open(filename, "r") as f:
        data = f.read()
    return data

def escrever_arquivo(filename,dados):
    with open(filename, "wb") as f:
        # escreve os dados no arquivo em bytes
        f.write(dados)
def escrever_arquivo_txt(filename,dados):
    with open(filename, "w") as f:
        # escreve os dados no arquivo 
        f.write(dados)

def to_ascii(text):
    ascii_values = [ord(character) for character in text]
    return ascii_values

def main():
        # Cria um objeto parser para lidar com os argumentos passados via linha de comando
        parser = argparse.ArgumentParser(description="Compressão deHuffman - Análise de frequência de símbolos e compressão de Huffman")
        # Adiciona argumentos ao parser
        parser.add_argument("arquivo", type=str, help="Arquivo a ser processado (comprimido, descomprimido ou para apresentar a tabela de símbolos)")
        parser.add_argument("-s", action="store_true", help="Realiza apenas a análise de frequência e imprime a tabela de símbolos")
        parser.add_argument("-c", action="store_true", help="Realiza a compressão")
        parser.add_argument("-d", action="store_true", help="Realiza a descompressão")
        # Faz o parser dos argumentos passados via linha de comando
        args = parser.parse_args()
        # Verifica se o argumento -s foi passado
        if args.s:
            caminho_arquivo = args.arquivo
            arquivo=ler_arquivo_txt(caminho_arquivo)
            dados=Calcular_probabilidade(arquivo)
            simbolos = dados.keys()

            nos = []

            for simbolo in simbolos:
                nos.append(Huff(dados.get(simbolo),simbolo))

            while len(nos) > 1:
                 nos = sorted(nos, key=lambda x: x.frequencia)
                 direita= nos[0]
                 esquerda = nos[1]
                 direita.digito = 0
                 esquerda.digito = 1

                 novono = Huff(esquerda.frequencia+direita.frequencia, esquerda.simbolo+direita.simbolo,esquerda,direita)
                 nos.remove(esquerda)
                 nos.remove(direita)
                 nos.append(novono)
            print("simbolo | frequencia | frequencia relativa | ascii | codigos huff")
            for simbolo, frequencia in dados.items():
                print(f"{simbolo}   {frequencia}   {round(frequencia/len(dados),3)}   {to_ascii(simbolo)}   {calcular_codigos(nos[0])}")
            return
        # Verifica se o argumento -c foi passado
        if args.c:
            caminho_arquivo = args.arquivo
            if not os.path.isfile(caminho_arquivo):
                print("Erro: O arquivo especificado não existe.")
                return
             # Lê o arquivo, realiza a análise de frequência de símbolos, cria a árvore de Huffman e obtém os códigos
            dados = ler_arquivo_txt(args.arquivo)
            codificacao=huffman_compilar(dados)
            escrever_arquivo(args.arquivo + ".huff", codificacao)

            nome_arquivo_saida = caminho_arquivo + ".huff"

            tamanho_original = os.path.getsize(caminho_arquivo)  # Obtém o tamanho do arquivo original
            tamanho_comprimido = os.path.getsize(nome_arquivo_saida)  # Obtém o tamanho do arquivo comprimido
            taxa_compressao = (1 - tamanho_comprimido / tamanho_original) * 100  # Calcula a taxa de compressão em porcentagem

            print(f"Arquivo comprimido com sucesso: {nome_arquivo_saida}")
            print(f"Tamanho original: {tamanho_original} bytes")
            print(f"Tamanho comprimido: {tamanho_comprimido} bytes")
            print(f"Taxa de compressão: {taxa_compressao:.2f}%")

            print(f"Comprimido com sucesso: {os.path.getsize(args.arquivo + '.huff')} bytes")

            return
         # Verifica se o argumento -d foi passado
        if args.d:
             caminho_arquivo = args.arquivo

             arquivo=args.arquivo
             arquivo=arquivo.replace(".huff","")
             dados = ler_arquivo_txt(arquivo)
             decodificacao = huffman_descompilar(dados)
             #print(decodificacao)
             escrever_arquivo_txt(args.arquivo + ".dec", decodificacao)

             nome_arquivo_saida = caminho_arquivo + ".dec"

             tamanho_original = os.path.getsize(caminho_arquivo)  # Obtém o tamanho do arquivo original
             tamanho_descomprimido = os.path.getsize(nome_arquivo_saida)  # Obtém o tamanho do arquivo comprimido
             taxa_descompressao = (1 - tamanho_original / tamanho_descomprimido) * 100  # Calcula a taxa de compressão em porcentagem

             print(f"Arquivo descomprimido com sucesso: {nome_arquivo_saida}")
             print(f"Tamanho original: {tamanho_original} bytes")
             print(f"Tamanho descomprimido: {tamanho_descomprimido} bytes")
             print(f"Taxa de decompressão: {taxa_descompressao:.2f}%")

             print(f"desComprimido com sucesso: {os.path.getsize(args.arquivo + '.dec')} bytes")
             
        return
if __name__ == "__main__":
    main()

