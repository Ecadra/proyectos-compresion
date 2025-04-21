from django.shortcuts import render

# Create your views here.
def compresion_lz78(texto):
    diccionario = {"":0}
    tamaño_diccionario = 1
    pasado = ""
    texto_comprimido = []
    for car in texto:
        pasado_actual = pasado + car
        if pasado_actual in diccionario:
            pasado = pasado_actual
        else:
            texto_comprimido.append((diccionario[pasado],car))
            diccionario[pasado_actual] = tamaño_diccionario
            tamaño_diccionario+=1
            pasado=""
    if pasado:
        texto_comprimido.append((diccionario[pasado],''))

    descompresion = descompresion_lz78(texto_comprimido)
    return{
        'texto_comprimido':texto_comprimido,
        'diccionario_compresion':diccionario,
        'tamaño_final_compresion':len(texto_comprimido),
        'tamaño_original_compresion':len(texto),
        'descompresion': descompresion
    }

def descompresion_lz78(texto_comprimido):
    diccionario = {0:""}
    tamaño_diccionario = 1
    resultado = []

    for index, car in texto_comprimido:
        entrada = diccionario[index]
        nueva_cadena = entrada + car
        resultado.append(nueva_cadena)
        diccionario[tamaño_diccionario] = nueva_cadena
        tamaño_diccionario += 1

    resultado = "".join(resultado)
    return{
        'texto_descomprimido':resultado,
        'diccionario_descompresion': diccionario,
    }
def index(request):
    if request.method == 'POST' and request.FILES['file']:
        archivo_subido = request.FILES['file']
        texto = archivo_subido.read().decode('utf-8').strip()
        contexto = compresion_lz78(texto)
        return render(request, 'lz78/resultados.html',{'contexto': contexto, 'texto': texto})
    return render(request,'lz78/upload.html')

if __name__ == "__main__":
    texto_original = "abracadabra"
    print(texto_original)
    texto_comprimido = compresion_lz78(texto_original)
    print(texto_comprimido['texto_comprimido'])