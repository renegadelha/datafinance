t1 = 'eu quero ir embora daqui'
t2 = 'ire'
tam = len(t2)
teste = False
for i in range(0, len(t1)):
    if (t1[i] == t2[0] and i + len(t2) <= len(t1)):
        if(len(t2) == 1):
            teste = True
        else:
            for j in range(1, len(t2)):
                if(t1[i+j] == t2[j]):
                    teste = True
                else:
                    teste = False

    if(teste):
        break
if(teste):
    print('t2 está contida dentro de t1')
else:
    print('t2 NAO está contida dentro de t1')