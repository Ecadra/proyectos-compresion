from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html', {
        'apps': [
            {'name': 'Entropia', 'url': 'entropia:index'},
            {'name': 'Estadistico', 'url': 'estadistico:index'},
            {'name': 'Huffman', 'url': 'huffman:index'},
            {'name': 'Aritmetica', 'url': 'aritmetica:index'},
        ]
    })