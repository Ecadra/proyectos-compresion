from django.shortcuts import render
from collections import Counter



def delta_codec(texto):
    old_array=[]
    textDecoded=[]
    new_array=[]
    decoded_array=[]

    for char in texto:
        old_array.append(ord(char))
    
    new_array.append(old_array[0])
    aux=0
    while aux < len(old_array)-1:
        if aux >= len(old_array)-1:
            #print(old_array[aux],' - ',old_array[aux-1])
            resta=old_array[aux]-old_array[aux-1]
            new_array.append(resta)
        else:
            #print(old_array[aux+1],' - ',old_array[aux])
            resta=old_array[aux+1]-old_array[aux]
            new_array.append(resta)
        aux+=1

    aux=0
    decoded_array.append(new_array[0])
    while aux < len(new_array)-1:
        suma= decoded_array[aux]+ new_array[aux+1]
        decoded_array.append(suma)
        aux+=1
    
    for num in decoded_array:
        textDecoded.append(chr(num))
    
    textDecoded=''.join(textDecoded)

    tabla_interfaz=list(zip(old_array, new_array, decoded_array))
    return {
        'tabla_interfaz':tabla_interfaz,
        'texto': texto,
        'textDecoded':textDecoded
    }
 
def index(request):
    
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            texto = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return render(request, 'delta/error.html', {'error':'Formato de archivo no válido'})
        delta=delta_codec(texto)
        return render(request,'delta/resultados.html',{'delta':delta, 'texto':texto})

    return render(request, 'delta/upload.html')