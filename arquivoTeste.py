def soma(vetor):
    if vetor == []:
        return 0
    else:
        return vetor[0] + soma(vetor[1:])

x = [2,4,6]

print(soma(x))