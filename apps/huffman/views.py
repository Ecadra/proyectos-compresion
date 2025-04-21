from django.shortcuts import render
from django.http import HttpResponse
from collections import Counter
import heapq 


class Node(object):

    def __init__(self, symbol=None, frequency=None, priority=0): #Agregar una prioridad al nodo
        self.symbol=symbol
        self.frequency=frequency
        self.priority=priority
        self.left=None
        self.rigth=None
    def __lt__(self, other):
        if self.frequency == other.frequency:
            return self.priority <  other.priority
        return self.frequency<other.frequency



def huffman_code_tree(listFreq):

    priority=0
    arregloNodos=[]

    for char,freq in listFreq:
        arregloNodos.append(Node(char,freq,priority))
        #print(arregloNodos)
        priority= priority+1
        #print(priority)
    
    heapq.heapify(arregloNodos)

    while len(arregloNodos)>1:
        left_child = heapq.heappop(arregloNodos)
        right_child = heapq.heappop(arregloNodos)
        merge_node=Node(frequency=left_child.frequency + right_child.frequency) 
        #print(merge_node)
        merge_node.left=left_child
        merge_node.rigth=right_child
        heapq.heappush(arregloNodos, merge_node)

    return arregloNodos[0]

def get_frequency(texto):
    
    freq = {}
    for c in texto:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1])
    return freq

def create_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol]=code
        create_codes(node.left, code +"0", huffman_codes)
        create_codes(node.rigth, code +"1", huffman_codes)
    return huffman_codes

def code_text(texto, huffmanCode):
    codificado = []
    for caracter in texto:
        if caracter in huffmanCode:
            codificado.append(huffmanCode[caracter])
    return ''.join(codificado)

def decode_text(coded, huffmanCode):#huffmanCode es un diccionario
    decoded=[]
    current_code=""
    #Invertir el diccionario
    reversed_list={code:char for char, code in huffmanCode.items()}
    for bit in coded:
        current_code += bit#Variable que guarda cada bit de la cadena codificada
        #print(current_code)
        if current_code in reversed_list:#Aqui se busca por keys
            decoded.append(reversed_list[current_code])
            current_code=""
    return''.join(decoded)
    
'''
texto="MI MAMA ME MIMA"
frequency=get_frequency(texto) 
print(frequency)
root= huffman_code_tree(frequency)
huffmanCodes=create_codes(root)
print(huffmanCodes)
coded=code_text(texto,huffmanCodes)
print(coded)
decoded=decode_text(coded,huffmanCodes)
print(decoded)
'''
def index(request):
   
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            texto = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return render(request,"huffman/error.html", {'error':'Formato de archivo no válido'})
        
        frequency=get_frequency(texto)
        root= huffman_code_tree(frequency) 
        huffmanCodes=create_codes(root)
        coded=code_text(texto,huffmanCodes)
        decoded=decode_text(coded,huffmanCodes)
       
        return render(request, "huffman/resultados.html",{"texto": texto,"frequency":frequency, 'huffmanCodes': huffmanCodes, 'coded':coded, 'decoded':decoded})
    
    return render(request, "huffman/upload.html")
