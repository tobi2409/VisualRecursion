'''
Ziel ist es, einen WYSIWYG-Editor zu entwickeln
darin kann eine Rekursion in Form einer Baumstruktur modelliert werden
damit die Visualisierung gut verständlich ist, wird dort mit Beispiel-Nodes gearbeitet
diese Beispiel-Nodes haben aber keine Auswirkung auf den Algorithmus, sondern dienen lediglich der Visualisierung
wichtig ist, dass die deltas angegeben werden,
wobei man im Laufe der Entwicklung auch eine Mustererkennung entwickeln kann für die Übertragung von Beispiel-Nodes auf delta
'''

def appendChilds(lst, delta, bufferCallback=(lambda node: node['value']), combineCallback=(lambda node: node['value']),
        resultConditionCallback=(lambda node: node['childs'] == []), resultNodeCallback=(lambda node: node), expandOnEmptyDelta = False):
        
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

                node['value'] = combineCallback(node) # für Bottom-Up-Rekursion

                treeResult.append(node)

                if resultConditionCallback(node):
                    resultNode = resultNodeCallback(node)
                    if resultNode != None:
                        result.append(resultNodeCallback(node))

                result.extend(nextResult)

        return treeResult, result

    root = factorNode(None, -1, -1, 0, [], None)
    childs, result = _appendChilds(lst, delta)
    root['childs'].extend(childs)
    return root, result

def divideAndConquer(lst, mergeChildsCallback, resultNodeCallback=(lambda node: node)):

    def delta(node, lst, originalLst):
        if len(node['value']) <= 1:
            return []

        mid = len(node['value']) // 2
        return [node['value'][:mid], node['value'][mid:]]

    def combineCallback(node):
        if len(node['childs']) == 0:
            return node['value']

        childs = node['childs']

        return mergeChildsCallback(childs, node)

    def resultConditionCallback(node):
        return node['layer'] == 1

    return appendChilds([lst], delta,
        combineCallback=combineCallback,
        resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True)

def getObject(id):
    if id == None:
        return None

    import ctypes
    return ctypes.cast(id, ctypes.py_object).value