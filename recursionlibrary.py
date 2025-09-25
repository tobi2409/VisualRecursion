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

    def _appendChilds(_lst, delta, layer=1, parent=None, originalLst=lst):
        treeResult = []
        result = []

        if type(_lst) != list:
            return [], []

        _lstSize = len(_lst)

        for i, e in enumerate(_lst):
            node = factorNode(e, i, _lstSize, layer, [], parent)

            # das Value kann sich nochmal entscheidend verändern bzgl. delta und Child-Erzeugung
            node['value'] = bufferCallback(node) # Buffer-Informationen beim Top-Down

            deltaed = delta(node, _lst, originalLst)

            if deltaed != [] or expandOnEmptyDelta: # Node aufnehmen, wenn Kinder existieren ODER wir auch Blätter erzwingen wollen
                childNodes, nextResult = _appendChilds(deltaed, delta, layer=layer + 1, parent=id(node), originalLst=lst)
                node['childs'].extend(childNodes)

                node['value'] = combineCallback(childNodes, node) # für Bottom-Up-Rekursion

                treeResult.append(node)
                
                childsHandler(node['childs'], node) # childs-Input (u.a. für Sibling-Management des nächsten Layers) holen und Output in node eintragen

                if node['childs'] == []:
                    result.append(node)
                result.extend(nextResult)

        return treeResult, result

    root = factorNode(None, -1, -1, 0, [], None)
    childs, result = _appendChilds(lst, delta)
    root['childs'].extend(childs)
    return root, result

def getObject(id):
    if id == None:
        return None

    import ctypes
    return ctypes.cast(id, ctypes.py_object).value