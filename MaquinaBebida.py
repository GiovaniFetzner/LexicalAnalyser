while 1:
    produto = False
    while produto == False:
        print('\x1b[0;30;47m''             BEBIDAS                 ''\x1b[0m')
        print('1 - Água Mineral s/gás........R$ 3,00')
        print('2 - Água Mineral c/gás........R$ 3,00')
        print('3 - Coca-Cola.................R$ 4,00')
        print('4 - Pepsi.....................R$ 4,00')

        Numero_Produto = int(input('\x1b[0;30;47m''  Selecione qual item deseja comprar:   ''\x1b[0m'))
        import time
        time.sleep(1.5)

        if Numero_Produto == 1 or Numero_Produto == 2:
            Valor_Pagar = 3
            produto = True

        elif Numero_Produto == 3 or Numero_Produto == 4:
            Valor_Pagar = 4
            produto = True

        else:
            print ('\x1b[1;37;41m''            Botão Inválido            ''\x1b[0m')
            time.sleep(7.0)
            import os
            os.system('cls') or None

    time.sleep(2.0)

    print ('Esta máquina não devolve troco, caso coloque um valor superior ao valor descrito do produto, será desconsiderado pela máquina')
    time.sleep (4.0)
    print ('O valor que deve ser pago é R$',Valor_Pagar,',00. O leitor de moeda, só aceita moeda de R$ 1,00 e leitor de nota, só aceita nota de R$ 2,00')
    time.sleep (4.0)

    tentativas = int(2)

    while tentativas  >= 0:
        Leitor_Moedas = int(input('Digite a quantidade de moedas de R$: 1,00: '))
        Leitor_Notas = int(input('Digite a quantidade de notas de R$: 2,00: '))

        Valor_Inserido = int((Leitor_Moedas * 1) + (Leitor_Notas * 2))

        if Valor_Inserido < Valor_Pagar:
            tentativas = tentativas - 1
            print ('\x1b[1;37;41m''          Saldo Insuficiente          ''\x1b[0m')
            time.sleep (3.0)

        else:
            print ('\x1b[1;37;42m''          Saldo Suficiente           ''\x1b[0m')
            time.sleep (3.0)
            print ('\x1b[1;37;42m''         Retire seu produto          ''\x1b[0m')
            break

    time.sleep (3.0)
    print('Sessão encerrada')
    time.sleep(1.5)
    import os
    os.system('cls') or None
    time.sleep(5)