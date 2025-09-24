'''
Ziel ist es, einen WYSIWYG-Editor zu entwickeln
darin kann eine Rekursion in Form einer Baumstruktur modelliert werden
damit die Visualisierung gut verständlich ist, wird dort mit Beispiel-Nodes gearbeitet
diese Beispiel-Nodes haben aber keine Auswirkung auf den Algorithmus, sondern dienen lediglich der Visualisierung
wichtig ist, dass die deltas angegeben werden,
wobei man im Laufe der Entwicklung auch eine Mustererkennung entwickeln kann für die Übertragung von Beispiel-Nodes auf delta
'''

def appendChilds(lst, delta, childsHandler=(lambda childs, node: None), bufferCallback=(lambda node: None), combineCallback=(lambda childs, node: None)):
    def factorNode(value, currentListIndex, lstSize, layer, childs, parent):
        return {'value': value, 'currentListIndex': currentListIndex, 'listSize': lstSize, 'layer': layer, 'childs': childs, 'parent': parent}

    def _appendChilds(lst, delta, layer=1, parent=None):
        result = []

        nextLayer = layer + 1

        lstSize = len(lst)

        for i, e in enumerate(lst):
            node = factorNode(e, i, lstSize, layer, [], parent)

            node['value'] = bufferCallback(node) # Buffer-Informationen beim Top-Down

            deltaed = delta(node, lst)
            if deltaed != []:
                #relationLessNode = factorNode(e, i, lstSize, layer, [], None)

                childNodes = _appendChilds(deltaed, delta, layer=nextLayer, parent=id(node))
                node['childs'].extend(childNodes)

                node['value'] = combineCallback(childNodes, node) # für Bottom-Up-Rekursion

                result.append(node)
                childsHandler(node['childs'], node) # childs-Input (u.a. für Sibling-Management des nächsten Layers) holen und Output in node eintragen

        return result

    root = factorNode(None, -1, -1, 0, [], None)
    root['childs'].extend(_appendChilds(lst, delta))
    return root

def getObject(id):
    if id == None:
        return None

    import ctypes
    return ctypes.cast(id, ctypes.py_object).value

from json import dumps

def fak(n):
    def delta(node, lst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def bufferCallback(node):
        return node['value']

    def combineCallback(childNodes, node):
	    return node['value'] * childNodes[0]['value'] if len(childNodes) != 0 else 1

    tree = appendChilds([n], delta, bufferCallback=bufferCallback, combineCallback=combineCallback)
    print(dumps(tree, indent=2))

#fak(5)

def sum(n):
    def delta(node, lst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(childNodes, node):
        return node['value'] + childNodes[0]['value'] if len(childNodes) != 0 else node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback), indent=2))

#sum(5)

def fib(n):
    def delta(node, lst):
        return [node['value'] - 1, node['value'] - 2] if node['value'] - 1 >= 0 else []

    def bufferCallback(node):
        return node['value']

    def combineCallback(childNodes, node):
        return childNodes[0]['value'] + childNodes[1]['value'] if len(childNodes) == 2 else 1

    print(dumps(appendChilds([n], delta, bufferCallback=bufferCallback, combineCallback=combineCallback), indent=2))

#fib(7)

"""
Angenommen, ein Kind kann eine Treppe mit s Stufen erklimmen, indem es entweder 1, 2, ..., k
Stufen in einem einzigen Schritt nimmt. Berechnen Sie alle unterschiedlichen Schrittfolgen, mit
denen das Kind genau die s Stufen der Treppe erklimmt.
"""
def steps(s):
    def delta(node, lst):
        return [i for i in range(1, s + 1)] if node['value'] < s + 1 else []

    def bufferCallback(node):
        return node['value'] + (getObject(node['parent'])['value'] if node['parent'] != None else 0)

    def combineCallback(childNodes, node):
        return node['value']
        
    print(dumps(appendChilds([i for i in range(1, s + 1)], delta, bufferCallback=bufferCallback, combineCallback=combineCallback), indent=2))

steps(5)