def imprimirMatriz(matriz: list):
    for i in range(n): 
        renglon = "|"
        for j in range(n): 
            renglon +=" "+str(matriz[i][j])+" "
        renglon += "|"
        print(renglon)
    print("")

def imprimirMatrizYAdjunta(n: int, matriz: list, adjunta: list):
    for i in range(n): 
        renglon = "|"
        for j in range(n): 
            renglon +=" "+str(matriz[i][j])+" "
        renglon += "|"
        for j in range(n): 
            renglon += " "+str(adjunta[i][j])+" "
        renglon += "|"
        print(renglon)

def validarSN()->bool: 
    sn = ""
    while sn != "s" and sn != "n": 
        sn = input("Desea ingresar una matriz? s/n: ").lower()
    return sn == "s"

def numEcuaciones()->int: 
    n = -1
    while n < 0: 
        try: 
            n = int(input("Ingrese el número de ecuaciones e incognitas (0 para salir): "))
        except ValueError: 
            print("-"*20+"\nEntrada inválida, intente otra vez\n")
        else: 
            print("-"*20)
            return n

def validarValor(x: str)->float: 
    while True: 
        try: 
            val = float(input(x))
        except ValueError: 
            print("-"*20+"\nEntrada inválida, intente otra vez\n")
        else:
            return val

def ingresarEcuaciones(n: int)->tuple:
    matriz = [[0 for j in range(n)] for i in range(n)]
    identidad = [[0 for i in range(n)] for j in range(n)]
    vector = [0 for i in range(n)]
    for i in range(n): 
        ecuacacion = ""
        print("Ecuación #"+str(i+1))
        for j in range(n): 
            matriz[i][j] = validarValor("Coeficiente de x"+str(j+1)+": ")
            if j > 0 and matriz[i][j]>=0: 
                ecuacacion+="+"
            ecuacacion += str(matriz[i][j])+"x"+str(j+1)+" "
            if(i == j): 
                identidad[i][j] = 1
        ecuacacion += "= "
        vector[i] = validarValor(ecuacacion)
        
    return matriz, vector, identidad

def montante(n: int, matriz: list, adjunta: list, pivote_ant=1.0, pivote_act=0)->list:
    nueva_matriz = [["x" for i in range(n)] for j in range(n)]
    nueva_adjunta = [["x" for i in range(n)] for j in range(n)]
    print("-"*20+"\n")
    imprimirMatrizYAdjunta(n, matriz, adjunta)
    print("\nPivote anterior = "+str(pivote_ant))
    print("Pivote actual = "+str(matriz[pivote_act][pivote_act])+"\n")
    for i in range(n): 
        for j in range(n): 
            if i == pivote_act:
                nueva_matriz[i][j] = matriz[i][j]
                nueva_adjunta[i][j] = adjunta[i][j]
            else: 
                if j == pivote_act: 
                    nueva_matriz[i][j] = 0
                else:
                    try: 
                        nueva_matriz[i][j] = (matriz[pivote_act][pivote_act]*matriz[i][j]-matriz[pivote_act][j]*matriz[i][pivote_act])/pivote_ant
                    except ZeroDivisionError: 
                        print("Ocurrió una división entre cero en el elemento "+str(i+1)+", "+str(j+1)+" de la nueva matriz")
                        imprimirMatrizYAdjunta(n, matriz, adjunta)
                        print("=>")
                        nueva_matriz[i][j] = "x"
                        imprimirMatrizYAdjunta(n, nueva_matriz, nueva_adjunta)
                        return []

                try: 
                    nueva_adjunta[i][j] = (matriz[pivote_act][pivote_act]*adjunta[i][j]-adjunta[pivote_act][j]*matriz[i][pivote_act])/pivote_ant
                except ZeroDivisionError: 
                    print("Ocurrió una división entre cero en el elemento "+str(i+1)+", "+str(j+1)+" de la nueva matriz adjunta")
                    imprimirMatrizYAdjunta(n, matriz, adjunta)
                    print("=>")
                    nueva_adjunta[i][j] = "x"
                    imprimirMatrizYAdjunta(n, nueva_matriz, nueva_adjunta)
                    return []
    #Recursivo
    if pivote_act + 1 == n: 
        print("-"*20)
        imprimirMatrizYAdjunta(n, nueva_matriz, nueva_adjunta)
        valida = True
        determinante = nueva_matriz[0][0]
        for i in range(n): 
            for j in range(n): 
                if i == j: 
                    if nueva_matriz[i][j] != determinante:
                        valida = False
                        break
                elif nueva_matriz[i][j] != 0:
                        valida = False
                nueva_adjunta[i][j] = nueva_adjunta[i][j]/determinante
        if(valida):
            print("\nDeterminante: "+str(determinante)+"\n")
            print("Matriz inversa: ")
            imprimirMatriz(nueva_adjunta)
            return nueva_adjunta
        else: 
            print("Matriz inválida")
            return []
    else: 
        return montante(n, nueva_matriz, nueva_adjunta, matriz[pivote_act][pivote_act], pivote_act+1)

def calcularX(n, matriz: list, vector: list):
    for i in range(n): 
        x = 0
        for j in range(n): 
            x += vector[j]*matriz[i][j]
        print("x"+str(i+1)+" = "+str(x))
    print("")

if __name__=="__main__": 
    while(validarSN()):
        n = numEcuaciones() 
        if(n > 0): 
            matriz, vector, identidad= ingresarEcuaciones(n)
            inversa = montante(n, matriz, identidad)
            if len(inversa) > 0: 
                calcularX(n, inversa, vector)