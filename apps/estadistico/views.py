# views.py
from django.shortcuts import render
from django.http import JsonResponse
import os
from collections import Counter
import math

def calcular_estadisticas(texto):
    # Calcular la frecuencia de cada carácter
    frecuencia = Counter(texto)
    caracteres_ordenados = sorted(frecuencia.keys())
    total_caracteres = sum(frecuencia.values())

    # Inicializar listas para la tabla de frecuencias
    caracteres = []
    frec_absolutas = []
    frec_absolutas_acum = []
    frec_relativas = []
    frec_relativas_acum = []

    # Calcular frecuencias absolutas, relativas y acumuladas
    acumulado_absoluto = 0
    acumulado_relativo = 0
    for caracter in caracteres_ordenados:
        frec_abs = frecuencia[caracter]
        frec_rel = frec_abs / total_caracteres

        acumulado_absoluto += frec_abs
        acumulado_relativo += frec_rel

        caracteres.append(caracter)
        frec_absolutas.append(frec_abs)
        frec_absolutas_acum.append(acumulado_absoluto)
        frec_relativas.append(frec_rel)
        frec_relativas_acum.append(acumulado_relativo)

    # Crear la tabla de frecuencias
    tabla_frecuencias = list(zip(caracteres, frec_absolutas, frec_absolutas_acum, frec_relativas, frec_relativas_acum))

    # Calcular medidas de tendencia central
    media = total_caracteres / len(frecuencia)
    mediana = frec_absolutas_acum[len(frec_absolutas_acum) // 2]
    max_frecuencia = max(frecuencia.values())
    caracter_mas_repetido= [character for character, frec in frecuencia.items() if frec == max_frecuencia]
    moda = f'El caracter más repetido en el texto es: {caracter_mas_repetido}'

    # Calcular medidas de dispersión
    rango = max(frec_absolutas) - min(frec_absolutas)
    varianza = sum((frec - media) ** 2 for frec in frec_absolutas) / len(frec_absolutas)
    desviacion_estandar = math.sqrt(varianza)

    return {
        'tabla_frecuencias': tabla_frecuencias,
        'media': media,
        'mediana': mediana,
        'moda': moda,
        'rango': rango,
        'varianza': varianza,
        'desviacion_estandar': desviacion_estandar
    }

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        texto = uploaded_file.read().decode('utf-8')

        estadisticas = calcular_estadisticas(texto)

        return render(request, 'estadistico/resultados.html', {'estadisticas': estadisticas, 'texto': texto})
    return render(request, 'estadistico/upload.html')