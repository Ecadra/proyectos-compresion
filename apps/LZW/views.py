from django.shortcuts import render
from collections import Counter

def compress(texto):

    dictionary=list(Counter(texto))#*Caracteres de todo el texto
    output = []
    past = []
    contador = len(texto)
    presentList=[]
    futureList = []
    decoded=[]
    
    for present in texto:
        #* #1- Si no hay nada en el pasado el presente se queda igual, de lo
        #* contrario el presente y el pasado se suman
        presentList.append(present)
        if len(past) == 0:
            future = present
            #print("Future = ", present)
        else:
            #print("Future = ", present, " + ", past[len(past)-1])
            future = past[len(past)-1] + present 
        futureList.append(future)    
        if future not in dictionary: #*Si el futuro no esta el diccionario
            dictionary.append(future)#*agregar el futuro al diccionario
            output.append(dictionary.index(past[len(past)-1]))#* Agregar el indice del último caracter guardado en el pasado
            past.append(present) #* Agregar el presente el pasado
        else:#* Si el caracter o caracteres ya estan en el diccionario
            past.append(future)#* Se agrega el futuro al pasado

        contador-=1 #? Contador para verificar el final del texto

        if(contador==0): #? En caso de que el texto llego al final se hace una última iteración para codificar el último caracter 
            future = past[len(past)-1] 
            print("Future = ", future)
            if future not in dictionary:
                dictionary.append(future)
                output.append(dictionary.index(past[len(past)-1]))
                past.append(present)
            else:
                output.append(dictionary.index(past[len(past)-1]))
                past.append(future)
    
    #? Decodificador:

    for index in output:
        decoded.append(dictionary[index])
    
    decoded=''.join(decoded)
    
    
    return {
        
        'decoded': decoded,
        'dictionary': dictionary,
        'past':past,
        'presentList':presentList,
        'futureList': futureList,
        'output':output
    }
    
    #return dictionary
print(compress("abacabaca"))
    
def index(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            texto = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return render(request, "LZW/error.html", {'error':'Formato de archivo no válido'})
        lzw=compress(texto)
        return render(request, 'LZW/resultados.html',{'LZW':lzw, 'texto': texto})
    
    return render(request, 'LZW/upload.html')