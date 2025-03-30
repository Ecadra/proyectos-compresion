from django.shortcuts import render
from django.http import HttpResponse


class NodeTree(object):

    def __init__(self, left = None, right = None):
        
        self.left = left
        self.right = right

    def children(self):
        return(self.left,self.right)
    
    def nodes(self):
        return(self.left,self.right)
    
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def huffman_code_tree(node, left = True, binString= ""):
    if type(node) is str:
        return {node: binString}
    (l,r) = node.children()
    d=dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

def get_frequency(texto):
    freq = {}
    for c in texto:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1],reverse=True)
    return freq

def create_nodes(freq):

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node=NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes,key=lambda x:x[1], reverse = True)

    return nodes

def code_text(texto, huffmanCode):
    codificado = []
    for caracter in texto:
        if caracter in huffmanCode:
            codificado.append(huffmanCode[caracter])
    return ''.join(codificado)

def index(request):
   
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        try:
            texto = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return render(request,"huffman/error.html", {'error':'Formato de archivo no válido'})
        
        freq=get_frequency(texto)
        node=create_nodes(freq)
        huffmanCode = huffman_code_tree(node[0][0])

        coded=code_text(texto, huffmanCode)

        return render(request,"huffman/resultados.html",{'texto': texto, 'nodes':node, 'huffmanCode' : huffmanCode, 'coded':coded, 'freq':freq})
    
    return render(request, "huffman/upload.html")
