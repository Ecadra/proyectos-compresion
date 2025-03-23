from django.shortcuts import render
from django.http import HttpResponse
from collections import Counter
import math


def calcular_entropia(texto):
    entropia=0
    #Calcular la frecuencia de cada carácter
    contarCadaLetra=Counter(texto)
    Numletras=len(texto)#Número total de letras del texto
    listCaracteres = []
    listRepeticionCaracteres = []
    listFrecuencias = []
    listLogaritmmos = []

    for nomcaracter in contarCadaLetra.keys():
        listCaracteres.append(nomcaracter)

    for caracter in contarCadaLetra.values():#Recorre los valores de las letras
        listRepeticionCaracteres.append(caracter)
        frecuencia=caracter/Numletras #Calcula la frecuencia del caracter
        listFrecuencias.append(frecuencia)
        #print(round(frecuencia,4)) #Imprime la frecuencia del caracter redondeada a 4 decimales
        logbase2=math.log(frecuencia,2)#Calcula el logaritmo en base 2 de la frecuencia
        listLogaritmmos.append(logbase2)
        #print(round(logbase2,4))
        entropia+=-(frecuencia*logbase2)#frecuencia*logaritmo en base 2 de la frecuencia y luego se suma para sacar la entropia
    
    tabla_frecuencias = list(zip(listCaracteres,listRepeticionCaracteres, listFrecuencias, listLogaritmmos))
    resultado = math.ceil(entropia)
    
    return{
        'tabla_frecuencias': tabla_frecuencias,
        'entropia': resultado
    }
    

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            texto = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return render(request, 'entropia/error.html', {'error':'Formato de archivo no válido'})
        entropia=calcular_entropia(texto)
        return render(request,'entropia/resultados.html',{'entropia':entropia, 'texto':texto})

    return render(request, 'entropia/upload.html')

# Create your views here.
