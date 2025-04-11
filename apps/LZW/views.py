from django.shortcuts import render
from collections import Counter

def compress(texto):

    dictionary=list(Counter(texto))#*Caracteres de todo el texto
    output = []
    past = []
    contador = len(texto)

    decoded=[]
    
    for present in texto:
        #* #1- Si no hay nada en el pasado el presente se queda igual, de lo
        #* contrario el presente y el pasado se suman
        if len(past) == 0:
            future = present
            #print("Future = ", present)
        else:
            #print("Future = ", present, " + ", past[len(past)-1])
            future = past[len(past)-1] + present 

        if future not in dictionary: #*Si el futuro no esta el diccionario
            dictionary.append(future)#*agregar el futuro al diccionario
            output.append(dictionary.index(past[len(past)-1]))#* Agregar el indice del último caracter guardado en el pasado
            past.append(present) #* Agregar el presente el pasado
        else:#* Si el caracter o caracteres ya estan en el diccionario
            past.append(future)#* Se agrega el futuro al pasado

        contador-=1 #? Contador para verificar el final del texto

        if(contador==0): #? En caso de que el texto llego al final se hace una última iteración para codificar el último caracter 
            if len(past) == 0:
                future = present
                #print("Future = ", present)
            else:
            #print("Future = ", present, " + ", past[len(past)-1])
                future = past[len(past)-1] + present 
            if future not in dictionary:
                dictionary.append(future)
                output.append(dictionary.index(past[len(past)-1]))
                past.append(present)
            else:
                past.append(future)
    
    #? Decodificador:

    for index in output:
        decoded.append(dictionary[index])
    
    decoded=''.join(decoded)

    return output, dictionary, decoded


texto="COMPADRE NO COMPRO COCO"

print(compress(texto))


def index(request):

    return render(request, 'LZW/resultados.html')