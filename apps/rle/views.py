from django.shortcuts import render

# Create your views here.
def compresion_rle(texto):
    resultado_compresion = []
    car_actual = texto[0]
    repeticiones = 1

    for car in texto[1:]:
        if car == car_actual:
            repeticiones += 1
        else:
            resultado_compresion.append(f'{repeticiones}{car_actual}')
            car_actual = car
            repeticiones = 1
    resultado_compresion.append(f'{repeticiones}{car_actual}')
    return {
        'texto_comprimido': resultado_compresion,
        'texto_original':texto,
        'tamaño_original': len(texto),
        'tamaño_comprimido':len(''.join(resultado_compresion))
    }

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        archivo_subido = request.FILES['file']
        texto = archivo_subido.read().decode('utf-8').strip()
        contexto = compresion_rle(texto)
        return render(request, 'rle/resultados.html',{'contexto': contexto, 'texto': texto})
    return render(request,'rle/upload.html')