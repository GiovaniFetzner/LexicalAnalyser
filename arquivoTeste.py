#Exemplo com código funcional (divisão e conquista)
def soma(vetor):
    if vetor == []:
        return 0
    else:
        return vetor[0] + soma(vetor[1:])

x = [2, 4, 6]

print(soma(x))

# Exemplos adicionais

'''
Teste com muitos volumes
de palavras
'''

numero_inteiro = 42
numero_decimal = 3.14
texto_simples = "Ola mundo"
texto_com_aspas = "Texto com \"aspas\" internas"