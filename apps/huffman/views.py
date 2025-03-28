from django.shortcuts import render
from django.http import HttpResponse
import heapq
from collections import Counter

class Node:

    def __init__(self, symbol = None, frequency = None):
        self.symbol = symbol #Simbolo o valo del nodo
        self.frequency = frequency #
        self.left = None
        self.right = None

    def __lt__(self, other):#Esta función compara nodos segun su frecuencia 
        return self.frequency < other.frequency  #En huffman los nodos con menor frecuencia se procesan primero


def huffman_tree(dictionaryFrecuency):
     
    #Uso del modulo heapq para crear una lista de prioridades
    priority_queue = [Node(chars, f) for chars, f in dictionaryFrecuency.items()]
    heapq.heapify(priority_queue)

    #Este es el motor para contruir el arbol de huffman
    while len (priority_queue) > 1:   
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency = left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code = "", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)
    return huffman_codes

def get_frequency(texto):
    return dict(Counter(texto))
       

def index(request):
    return HttpResponse("El proyecto está inicializado aquí")

# Create your views here.
