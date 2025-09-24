'''
Ziel ist es, einen WYSIWYG-Editor zu entwickeln
darin kann eine Rekursion in Form einer Baumstruktur modelliert werden
damit die Visualisierung gut verständlich ist, wird dort mit Beispiel-Nodes gearbeitet
diese Beispiel-Nodes haben aber keine Auswirkung auf den Algorithmus, sondern dienen lediglich der Visualisierung
wichtig ist, dass die deltas angegeben werden,
wobei man im Laufe der Entwicklung auch eine Mustererkennung entwickeln kann für die Übertragung von Beispiel-Nodes auf delta
'''

def appendChilds(lst, delta, bufferCallback=(lambda node: node['value']), combineCallback=(lambda childs, node: node['value']), childsHandler=(lambda childs, node: None),
        expandOnEmptyDelta = False):
    def factorNode(value, currentListIndex, lstSize, layer, childs, parent):
        return {'value': value, 'currentListIndex': currentListIndex, 'listSize': lstSize, 'layer': layer, 'childs': childs, 'parent': parent}

    def _appendChilds(lst, delta, layer=1, parent=None):
        result = []

        lstSize = len(lst)

        for i, e in enumerate(lst):
            node = factorNode(e, i, lstSize, layer, [], parent)

            # das Value kann sich nochmal entscheidend verändern bzgl. delta und Child-Erzeugung
            node['value'] = bufferCallback(node) # Buffer-Informationen beim Top-Down

            deltaed = delta(node, lst)

            if deltaed != [] or expandOnEmptyDelta: # Node aufnehmen, wenn Kinder existieren ODER wir auch Blätter erzwingen wollen
                childNodes = _appendChilds(deltaed, delta, layer=layer + 1, parent=id(node))
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