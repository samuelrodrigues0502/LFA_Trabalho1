import math

from bs4 import BeautifulSoup as bs

class AutomatoFD:

    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    def limpaAfd(self):
        """Inicializa variáveis utilizadas no processsamento de cadeias*/"""
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    def criaEstado(self, id, inicial=False, final=False):
        id = int(id)
        if id in self.estados:
            return False
        self.estados = self.estados.union({id})
        if inicial:
            self.inicial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    def criaTransicao(self, origem, destino, simbolo):

        origem = int(origem)
        destino = int(destino)
        simbolo = str(simbolo)

        if not origem in self.estados:
            return False
        if not destino in self.estados:
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False
        self.transicoes[(origem, simbolo)] = destino
        return True

    def mudaEstadoInicial(self, id):

        id = int(id)
        if not id in self.estados:
            return
        self.inicial = id

    def mudaEstadoFinal(self, id, final):

        id = int(id)
        if not id in self.estados:
            return
        if final:
            self.finais = self.finais.union({id})
        else:
            self.finais = self.finais.difference({id})

    def move(self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                break
            if (self.__estadoAtual, simbolo) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                break
        return self.__estadoAtual

    def deuErro(self):
        return self.__deuErro

    def estadoAtual(self):
        return self.__estadoAtual

    def estadoFinal(self, id):
        return id in self.finais

    def __str__(self):

        s = 'AFD(E, A, T, i, F): \n'
        s += 'E = { '

        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += 'A = { '
        for a in self.alfabeto:
            s += "'{}', ".format(a)
        s += '} \n'
        s += 'T = { '
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({},'{}')-->{}, ".format(e, a, d)
        s += '} \n'
        s += 'i = {} \n'.format(self.inicial)
        s += 'F = { '
        for e in self.finais:
            s += '{}; '.format(str(e))
        s += '}'
        return s

def testeAFDresultante(afdResultante):
    cadeia = str(input('Insira a cadeia para teste: '))
    afdResultante.limpaAfd()
    parada = afdResultante.move(cadeia)
    if not afdResultante.deuErro() and afdResultante.estadoFinal(parada):
        print('Aceita cadeia "{}"'.format(cadeia))
    else:
        print('Rejeita cadeia "{}"'.format(cadeia))


def intercessaoAFDS(afd, afd2):
    # setando o mesmo alfabeto para os afds
    afdResultante = AutomatoFD(afd.alfabeto)

    # indice auxiliar
    id = 0

    # tupla que armazena o estado dos 2 afds de acordo com o índice
    estadoParaTupla = dict()
    # tupla que armazena de forma contrária para facilitar o acesso
    tuplaParaEstado = dict()

    for i in afd.estados:
        for j in afd2.estados:
            inicial = False
            final = False
            if i == afd.inicial and j == afd2.inicial:
                inicial = True
            # condição para determinar estados finais
            if i in afd.finais and j in afd2.finais:
                final = True
            afdResultante.criaEstado(id, inicial, final)
            estadoParaTupla[id] = (i, j)
            tuplaParaEstado[(i, j)] = id
            id = id + 1

    for est in afdResultante.estados:
        for simb in afdResultante.alfabeto:
            # váriavel auxiliar que armazena o estado da tupla de acordo com os estados dos afds
            estadoRepresentado = estadoParaTupla[est]
            # seta para qual estado os afds vão de acordo com o símbolo
            estAut1 = afd.transicoes[estadoRepresentado[0], simb]
            estAut2 = afd2.transicoes[estadoRepresentado[1], simb]
            # o destino do estdo do afd resultante é criado a partir dos estados dos afds
            idAfdResult = tuplaParaEstado[(estAut1, estAut2)]
            afdResultante.criaTransicao(est, idAfdResult, simb)

    cortarEstadosDisconexos(afdResultante)
    return afdResultante

def uniaoAFDS(afd, afd2):
    # setando o mesmo alfabeto para os afds
    afdResultante = AutomatoFD(afd.alfabeto)
    # indice auxiliar
    id = 0

    # tupla que armazena o estado dos 2 afds de acordo com o índice
    estadoParaTupla = dict()
    # tupla que armazena de forma contrária para facilitar o acesso
    tuplaParaEstado = dict()

    for i in afd.estados:
        for j in afd2.estados:
            inicial = False
            final = False
            if i == afd.inicial and j == afd2.inicial:
                inicial = True
            # condição para determinar estados finais
            if i in afd.finais or j in afd2.finais:
                final = True
            afdResultante.criaEstado(id, inicial, final)
            estadoParaTupla[id] = (i, j)
            tuplaParaEstado[(i, j)] = id
            id = id + 1

    for est in afdResultante.estados:
        for simb in afdResultante.alfabeto:
            estadoRepresentado = estadoParaTupla[est]
            estAut1 = afd.transicoes[estadoRepresentado[0], simb]
            estAut2 = afd2.transicoes[estadoRepresentado[1], simb]
            idAfdResult = tuplaParaEstado[(estAut1, estAut2)]
            afdResultante.criaTransicao(est, idAfdResult, simb)

    cortarEstadosDisconexos(afdResultante)
    return afdResultante


def complementoAFD(afd):
    print('ANTES:')
    print(afd, '\n')
    for est in afd.estados:
        if est not in afd.finais:
            afd.mudaEstadoFinal(est, True)
        else:
            afd.mudaEstadoFinal(est, False)
    print('DEPOIS:')
    return afd

def diferencaAFDS(afd, afd2):
    # setando o mesmo alfabeto para os afds
    afdResultante = AutomatoFD(afd.alfabeto)
    # indice auxiliar
    id = 0

    # fazendo o complemento do afd2 para realizarmos a diferenca
    print('AFD2 negado')
    complementoAFD(afd2)

    # tupla que armazena o estado dos 2 afds de acordo com o índice
    estadoParaTupla = dict()
    # tupla que armazena de forma contrária para facilitar o acesso
    tuplaParaEstado = dict()

    for i in afd.estados:
        for j in afd2.estados:
            inicial = False
            final = False
            if i == afd.inicial and j == afd2.inicial:
                inicial = True
            # condição para determinar estados finais
            if i in afd.finais and j in afd2.finais:
                final = True
            afdResultante.criaEstado(id, inicial, final)
            estadoParaTupla[id] = (i, j)
            tuplaParaEstado[(i, j)] = id
            id = id + 1

    for est in afdResultante.estados:
        for simb in afdResultante.alfabeto:
            estadoRepresentado = estadoParaTupla[est]
            estAut1 = afd.transicoes[estadoRepresentado[0], simb]
            estAut2 = afd2.transicoes[estadoRepresentado[1], simb]
            idAfdResult = tuplaParaEstado[(estAut1, estAut2)]
            afdResultante.criaTransicao(est, idAfdResult, simb)

    cortarEstadosDisconexos(afdResultante)
    return afdResultante

def estEquivAFD(afd):
    # Obtém o alfabeto do AFD.
    alfabeto = afd.alfabeto

    # Inicialização: Crie duas partições - uma para estados finais e outra para não finais.
    particoes = [set(afd.finais), set(afd.estados - afd.finais)]
    particoes_anteriores = []

    # Realiza a minimização até que as partições não mudem entre iterações.
    while particoes != particoes_anteriores:
        particoes_anteriores = particoes.copy()
        novas_particoes = []

        # Itera sobre as partições atuais.
        for particao in particoes:
            if len(particao) > 1:
                particoes_por_destino = {}

                # Itera sobre os estados na partição atual.
                for estado in particao:
                    transicoes_estado = []

                    # Itera sobre os símbolos do alfabeto.
                    for simbolo in alfabeto:
                        destino = afd.transicoes.get((estado, simbolo))
                        particao_destino = None

                        # Verifica em qual partição o estado de destino está.
                        for index, p in enumerate(particoes):
                            if destino in p:
                                particao_destino = index
                                break

                        transicoes_estado.append(particao_destino)

                    chave_transicoes = tuple(transicoes_estado)

                    # Cria partições com base nas transições.
                    if chave_transicoes not in particoes_por_destino:
                        particoes_por_destino[chave_transicoes] = set()
                    particoes_por_destino[chave_transicoes].add(estado)

                novas_particoes.extend(list(particoes_por_destino.values()))
            else:
                novas_particoes.append(particao)

        particoes = novas_particoes

    estados_equivalentes = set()

    # Identifica os estados equivalentes a partir das partições.
    for i in range(len(particoes)):
        if len(particoes[i]) > 1:
            estados_na_particao = list(particoes[i])
            for j in range(len(estados_na_particao)):
                for k in range(j + 1, len(estados_na_particao)):
                    estados_equivalentes.add((estados_na_particao[j], estados_na_particao[k]))

    # Retorna a lista de estados equivalentes.
    return list(estados_equivalentes)

def minimizaAfd(estEquiv, afd):
    # Cria um conjunto para armazenar os estados a serem removidos do AFD.
    estRemov = set()

    # Cria um dicionário para armazenar as novas transições do AFD.
    novas_transicoes = {}

    # Cria um mapeamento dos estados equivalentes usando a lista 'estEquiv'.
    equiv_map = {estEquiv[i][1]: estEquiv[i][0] for i in range(len(estEquiv))}

    # Adiciona os estados equivalentes ao conjunto 'estRemov'.
    for i in range(len(estEquiv)):
        estRemov.add(estEquiv[i][1])

    # Remove os estados equivalentes do conjunto de estados do AFD.
    afd.estados = afd.estados - estRemov

    # Remove os estados equivalentes do conjunto de estados finais do AFD.
    afd.finais = afd.finais - estRemov

    # Itera sobre as transições existentes no AFD.
    for origem, destino in afd.transicoes.items():
        novo_origem = origem
        novo_destino = destino

        # Verifica se o estado de origem precisa ser substituído pelo seu equivalente.
        if origem[0] in equiv_map:
            novo_origem = (equiv_map[origem[0]], origem[1])

        # Verifica se o estado de destino precisa ser substituído pelo seu equivalente.
        if destino in equiv_map:
            novo_destino = equiv_map[destino]

        # Atualiza o dicionário de novas transições com os pares (origem, destino) ajustados.
        novas_transicoes[novo_origem] = novo_destino

    # Atualiza as transições do AFD com as novas transições.
    afd.transicoes = novas_transicoes

    # Retorna o AFD minimizado.
    return afd

def EquivalenciaAFDS(afd1, afd2):
    tamIniAFD1 = len(afd1.estados)
    afd2Ini = afd2.inicial

    # cria os novos estados que receberam as transições do automato2
    for x in range(len(afd1.estados), len(afd2.estados) + len(afd1.estados)):
        afd1.criaEstado(x)

    # pega as transições do automato2 e tranfere para o automato1 de acordo com os novos estados gerados
    for i in afd2.transicoes.keys():
        novoEstado = int(i[0]) + tamIniAFD1
        novoVai = afd2.transicoes.get(i) + tamIniAFD1
        afd1.criaTransicao(novoEstado, novoVai, i[1])

    # adicina os estados finais do afd2 tbm no afd1
    for finais in afd2.finais:
        finais = int(finais) + tamIniAFD1
        afd1.finais.add(finais)
    List_estadosEqui = estEquivAFD(afd1)

    afd2Ini += tamIniAFD1
    print(10 * '=', 'Automato gerado para realizar a equivalencia de estados', 10 * '=', '\n', afd1)
    print(f'Estados que procuramos a equivalencia: ({afd1.inicial},{afd2Ini})')
    print('Estados Equivalentes: ', List_estadosEqui)

    # procura dentro da lista de equivalencias se os estados iniciais dos dois automatos são equivalentes
    for procura in List_estadosEqui:
        if procura[0] == afd1.inicial:
            if procura[1] == afd2Ini:
                print('Os automatos SÃO equivalentes')
            return
    print('Os automatos NÃO são equivalentes')

def cortarEstadosDisconexos(afd):
    listaVisitados = set()
    listaVisitados.add(afd.inicial)
    listaLargura = []
    listaLargura.append(afd.inicial)
    while len(listaLargura) > 0:
        elemento = listaLargura[0]
        for simbolo in afd.alfabeto:
            if (elemento, simbolo) in afd.transicoes and afd.transicoes[(elemento, simbolo)] not in listaVisitados:
                listaVisitados.add(afd.transicoes[(elemento, simbolo)])
                listaLargura.append(afd.transicoes[(elemento, simbolo)])
        listaLargura.pop(0)
    listaDisconexos = afd.estados.difference(listaVisitados)
    for disconexo in listaDisconexos:
        listaTransicaoMortas = []
        for key in afd.transicoes:
            if key[0] == disconexo:
                listaTransicaoMortas.append(key)
        for t in listaTransicaoMortas:
            afd.transicoes.pop(t)
        afd.finais.discard(disconexo)
        afd.estados.discard(disconexo)


def lerAFDxml(caminho):
    file = open(caminho, "r")
    dados = file.read()

    soup = bs(dados, 'xml')
    idEst = 0
    idFin = 0
    idIni = 0
    alf = ''
    # criando o alfabeto
    for tr in soup.findAll('transition'):
        if tr.text[5] not in alf:
            alf = alf + tr.text[5]
    afd = AutomatoFD(alf)
    # criando os estados
    for est in soup.findAll('state'):
        afd.criaEstado(idEst)
        idEst = idEst + 1
    # criando as transições
    for tr in soup.findAll('transition'):
        afd.criaTransicao(tr.text[1], tr.text[3], tr.text[5])
    # setando estado inicial
    for est in soup.findAll('state'):
        if est.find('initial'):
            afd.mudaEstadoInicial(idIni)
        idIni = idIni + 1
    # setando estados finais
    for est in soup.findAll('state'):
        if est.find('final'):
            afd.mudaEstadoFinal(idFin, True)
        idFin = idFin + 1

    return afd

def escreverArquivoXML(self, nomeArquivo):
    stateCount = len(self.estados)
    stateStep = math.sqrt(stateCount)
    stateX = 0
    stateY = 0

    parse = ''
    parse = parse + '<structure>\n'
    parse = parse + '\t<type>fa</type>\n'
    parse = parse + '\t<automaton>\n'
    for estado in self.estados:
        parse = parse + "\t\t<state id=\"{}\" name=\"q{}\">\n".format(estado, estado)
        parse = parse + "\t\t\t<x>{}</x>\n".format(stateX * 200)
        parse = parse + "\t\t\t<y>{}</y>\n".format(stateY * 200)
        if estado in self.finais:
            parse = parse + "\t\t\t<final/>\n"
        if estado == self.inicial:
            parse = parse + "\t\t\t<initial/>\n"
        parse = parse + "\t\t</state>\n"

        stateX += 1
        if stateX > stateStep:
            stateX = 0
            stateY += 1
    for t in self.transicoes:
        parse = parse + "\t\t<transition>\n"
        parse = parse + "\t\t\t<from>{}</from>\n".format(t[0])
        parse = parse + "\t\t\t<to>{}</to>\n".format(self.transicoes[t])
        parse = parse + "\t\t\t<read>{}</read>\n".format(t[1])
        parse = parse + "\t\t</transition>\n"

    parse = parse + "\t</automaton>\n"
    parse = parse + "</structure>"

    with open(str(nomeArquivo), 'w') as f:
        f.write(parse)
        f.close()
        print('AFD resultante salvo com sucesso!!!')
