from AFD import AutomatoFD, uniaoAFDS, intercessaoAFDS, diferencaAFDS, lerAFDxml, estEquivAFD, minimizaAfd, \
    EquivalenciaAFDS, complementoAFD, testeAFDresultante, escreverArquivoXML

def criaAfdManual(afd):
    print('Geração dos 2 AFDs para as operações')

    alf = input('Insira o alfabeto do afd em forma de string\n(Ex: ab -> a e b pertencem ao alfabeto):')
    afd = AutomatoFD(alf)

    qtdEst = int(input('\nInsira a quantidade de estados: '))

    for i in range(1, (qtdEst + 1)):
        afd.criaEstado(i)
    estIni = int(input('Insira o estado inicial: '))
    afd.mudaEstadoInicial(estIni)

    estFin = 0

    print('\nInsira o(s) estado(s) final(is) ou -1 para prosseguir')
    while estFin != -1:
        estFin = int(input('Insira o estado final: '))
        afd.mudaEstadoFinal(estFin, True)

    qtdTrans = len(alf)*qtdEst

    for i in range(qtdTrans):
        print('\nTransição', i + 1, '\n')
        origem = input('Insira a origem: ')
        destino = input('Insira o destino: ')
        simbolo = input('Insira o simbolo: ')

        afd.criaTransicao(origem, destino, simbolo)

    return afd


if __name__ == '__main__':

    print('Trabalho LFA - AFDs')

    opMenu = -1

    while opMenu != 0:
        print('\nMenu de opções')
        print('\n1 - Operações básicas entre 2 AFDS')
        print('2 - Minimização de AFD')
        print('3 - Verificar equivalência entre 2 AFDS')
        print('0 - Sair')

        opMenu = int(input('Selecione a opção desejada: '))

        if opMenu == 1:
            afd = AutomatoFD('')
            afd2 = AutomatoFD('')
            afdResult = AutomatoFD('')

            print('\nGeração dos 2 AFDs para as operações')

            print("Deseja criar o afd de forma manual ou ler um arquivo JFLAP?")
            print("1 - Manual")
            print("2 - JFLAP")
            opTipoCriaAfd = int(input('Selecione a opção desejada: '))

            print('Criando AFD 1\n')
            if(opTipoCriaAfd == 1):
                afd = criaAfdManual(afd)
            else:
                caminho = input("Insira o caminho do arquivo xml gerado pelo JFLAP: ")
                afd = lerAFDxml(caminho)
            print(afd)

            print('\nCriando AFD 2\n')
            if (opTipoCriaAfd == 1):
                afd2 = criaAfdManual(afd2)
            else:
                caminho = input("Insira o caminho do arquivo xml gerado pelo JFLAP: ")
                afd2 = lerAFDxml(caminho)
            print(afd2)

            print('\n1 - Realizar união')
            print('2 - Realizar intercessão')
            print('3 - Realizar diferença')
            print('4 - Realizar o complemento')
            print('-1 - Sair')

            opOperacao = int(input('Selecione a opção desejada: '))

            if opOperacao == 1:
                afdResult = uniaoAFDS(afd, afd2)
                print(afdResult)
                testeAFDresultante(afdResult)
            if opOperacao == 2:
                afdResult = intercessaoAFDS(afd, afd2)
                print(afdResult)
                testeAFDresultante(afdResult)
            if opOperacao == 3:
                afdResult = diferencaAFDS(afd, afd2)
                print(afdResult)
                testeAFDresultante(afdResult)
            if opOperacao == 4:
                opcao =int(input("Digite com qual automato você deseja realizar o complemento:\n1 - AFD1 \n2 - AFD2\n"))
                if opcao == 1:
                    afdResult = complementoAFD(afd)
                    print(afdResult)
                if opcao == 2:
                    afdResult = complementoAFD(afd2)
                    print(afdResult)
            salvar = int(input('Deseja salvar o afd resultante em um aruivo JFLAP?\n1 - Sim\n2 - Não\n'))
            if(salvar == 1):
                escreverArquivoXML(afdResult, 'afdResultOper.jff')


        if opMenu == 2:
            afd = AutomatoFD('')
            afdMin = AutomatoFD('')

            print("Deseja criar o afd de forma manual ou ler um arquivo JFLAP?")
            print("1 - Manual")
            print("2 - JFLAP")
            opTipoCriaAfd = int(input('Selecione a opção desejada: '))

            if (opTipoCriaAfd == 1):
                afd = criaAfdManual(afd)
            else:
                caminho = input("Insira o caminho do arquivo xml gerado pelo JFLAP: ")
                afd = lerAFDxml(caminho)

            print(f'\nAFD a ser minimizado\n{afd}')

            estEquiv = list(estEquivAFD(afd))
            print('\nSeus estados equivalentes: \n', estEquiv)

            afdMin = minimizaAfd(estEquiv, afd)
            print(f'\nAFD MÍNIMO\n{afd}')
            salvar = int(input('Deseja salvar o afd resultante em um aruivo JFLAP?\n1 - Sim\n2 - Não\n'))
            if (salvar == 1):
                escreverArquivoXML(afdMin, 'afdResultMin.jff')

        if opMenu == 3:
            afd = AutomatoFD('')
            afd2 = AutomatoFD('')

            print('\nGeração dos 2 AFDs para as operações')

            print("Deseja criar o afd de forma manual ou ler um arquivo JFLAP?")
            print("1 - Manual")
            print("2 - JFLAP")
            opTipoCriaAfd = int(input('Selecione a opção desejada: '))

            print('Criando AFD 1\n')
            if (opTipoCriaAfd == 1):
                afd = criaAfdManual(afd)
            else:
                caminho = input("Insira o caminho do arquivo xml gerado pelo JFLAP: ")
                afd = lerAFDxml(caminho)
            print(afd)

            print('\nCriando AFD 2\n')
            if (opTipoCriaAfd == 1):
                afd2 = criaAfdManual(afd2)
            else:
                caminho = input("Insira o caminho do arquivo xml gerado pelo JFLAP: ")
                afd2 = lerAFDxml(caminho)
            print(afd2)
            EquivalenciaAFDS(afd, afd2)
