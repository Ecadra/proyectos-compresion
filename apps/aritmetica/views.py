from django.shortcuts import render
from django.http import HttpResponse
from collections import Counter
from decimal import getcontext, Decimal

def comprimirTexto(texto):
    #Configuracion de precision a 100 decimales
    ctx = getcontext()
    ctx.prec = 750
    
    #Se obtiene la frecuencia de cada caracter
    frecuencia = Counter(texto)
    #Total de caracteres para obtener la probabilidad
    total_caracteres = sum(frecuencia.values())
    #Se ponen los caracteres en una lista
    caracteres = list(frecuencia.keys())
    #Se calcula la probabilidad de aparición de cada caracter
    probabilidad = [Decimal(frecuencia[caracter])/Decimal(total_caracteres) for caracter in caracteres]

    """ Calculo de rangos para cada caracter """
    rangos = [] #Se inicializa la lista de rangos vacía
    rango = Decimal('0') #Se inicializa el rango en 0
    for prob in probabilidad: #Para cada probabilidad
        rangos.append((rango, rango + prob)) #Se añade el rango correspondiente a la lista
        rango += prob #Se actualiza el rango con el límite superior del rango actual

    """ Construcción de la tabla para mostrar los caracteres, frecuencias, probabilidades y rangos """
    tablaCaracteres = list(zip(caracteres,
                               (frecuencia[caracter] for caracter in caracteres), 
                               probabilidad,
                               [(format(rango[0], '.15f'), format(rango[1], '.15f')) for rango in rangos]))


    """ Compresión del texto """
    #Variable para monitorear el avance del algoritmo
    compresion = ''
    #Rangos iniciales para la compresion
    rango_anterior=(Decimal('0'), Decimal('1'))

    #Listas para mostrar el avance de la compresion
    caracter_a_analizar=[]
    rangoAntiguo = []
    rangoNuevo = []
    #Para cada caracter en el texto
    for caracter in texto: 
        #Se obtiene el rango correspondiente al caracter actual
        rango_caracter = rangos[caracteres.index(caracter)]
        #Se calcula el rango de compresión, actualizando el rango inicial
        rangoAntiguo.append(rango_anterior)
        rango_anterior = (rango_anterior[0] + (rango_anterior[1] - rango_anterior[0]) * rango_caracter[0], 
                    rango_anterior[0] + (rango_anterior[1] - rango_anterior[0]) * rango_caracter[1] )
        #Se actualiza el texto comprimido con los el rango menor de compresion
        compresion = str(rango_anterior[0])
        rangoNuevo.append(rango_anterior)
        caracter_a_analizar.append(caracter)
    
    tablaCalculos = list(zip(
    caracter_a_analizar,
    [(format(rango[0], '.750f'), format(rango[1], '.750f')) for rango in rangoAntiguo],  # Formatear rangos antiguos
    [(format(rango[0], '.750f'), format(rango[1], '.750f')) for rango in rangoNuevo]     # Formatear rangos nuevos
))
    textoDescomprimido = descomprimirTexto(compresion,rangos,caracteres)
    return {
        'tablaCaracteres': tablaCaracteres,
        'tablaCalculos':tablaCalculos,
        'compresion': compresion,
        'textoDescomprimido':textoDescomprimido
    }

def descomprimirTexto(texto,rangos,caracteres):
    texto = Decimal(texto)
    texto_descomprimido = ''
    while True:
        encontrado = False
        for i, (lim_inf, lim_sup) in enumerate(rangos):
            if lim_inf <= texto < lim_sup:
                # Añadir el carácter correspondiente al texto descomprimido
                texto_descomprimido += caracteres[i]
                encontrado = True

                # Actualizar el valor comprimido
                ancho_rango = lim_sup - lim_inf
                texto = (texto - lim_inf) / ancho_rango

                break
        # Si no se encontró ningún rango, detener el proceso
        if not encontrado or texto == 0:
            break

    return texto_descomprimido


def index(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file=request.FILES['file']
        texto = uploaded_file.read().decode('utf-8')
        context = comprimirTexto(texto)
        return render(request, 'aritmetica/resultados.html', {'context': context, 'texto': texto})
    return render(request, 'estadistico/upload.html')
