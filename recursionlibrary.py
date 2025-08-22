def appendChilds(lst, delta, childsHandler=(lambda childs, node: None)):
    def factorNode(value, currentListIndex, lstSize, layer, childs, parent):
        return {'value': value, 'currentListIndex': currentListIndex, 'listSize': lstSize, 'layer': layer, 'childs': childs, 'parent': parent}

    def _appendChilds(lst, delta, layer=1, parent=None):
        result = []

        nextLayer = layer + 1

        lstSize = len(lst)

        for i, e in enumerate(lst):
            node = factorNode(e, i, lstSize, layer, [], parent)

            deltaed = delta(node, lst)
            if deltaed != []:
                relationLessNode = factorNode(e, i, lstSize, layer, [], None)
                node['childs'].extend(_appendChilds(deltaed, delta, layer=nextLayer, parent=relationLessNode))
                result.append(node)
                childsHandler(node['childs'], node) # childs-Input (u.a. für Sibling-Management des nächsten Layers) holen und Output in node eintragen

        return result

    root = factorNode(None, -1, -1, 0, [], None)
    root['childs'].extend(_appendChilds(lst, delta))
    return root

from json import dumps

def demo1():
    def delta(node, lst):
        return lst if node['layer'] <= 2 else []

    print(dumps(appendChilds([8,6,3,7], delta), indent=2))

#demo1()

def demo2():
    def delta(node, lst):
        return lst if node['layer'] <= 2 and (node['parent'] is None or node['value'] != node['parent']['value']) else []

    #print(dumps(appendChilds([8,6,3], filter), indent=2))
    appendChilds([8,6,3], delta)

#demo2()

def demo3():
    def delta(node, lst):
        return lst if node['layer'] <= 2 and (node['parent'] is None or node['value'] != node['parent']['value']) else []

    def childsHandler(childs, node):
        if node['layer'] != 1:
            return
        
        print('--------')

        for c in childs:
            print(f'CHILD-HANDLER for child - {c['value']} at layer {c['layer']}')

    #print(dumps(appendChilds([8,6,3], filter), indent=2))
    appendChilds([8,6,3], delta, childsHandler)

#demo3() 

def fak_TopDown(n):
    def delta(node, lst):
        return [node['value'] * (n - node['layer'])] if node['layer'] <= n else []

    print(dumps(appendChilds([n], delta), indent=2))

#fak_TopDown(5)

def fib_TopDown(n):
    def delta(node, lst):
        return [node['value'] + node['value'] - 1, node['value'] - 1 + node['value'] - 2] if node['layer'] <= n else []

    print(dumps(appendChilds([n], delta), indent=2))

fib_TopDown(5)

def fibonacci_demo(n):
    def delta(node, lst):
        # Rekursiv nur, wenn > 1
        if node['value'] > 1:
            return [node['value'] - 1, node['value'] - 2]
        else:
            return []

    def childsHandler(childs, node):
        # Basisfall: keine Kinder → Ergebnis ist der Wert selbst
        if not childs:
            node['result'] = node['value']
        else:
            # Sonst Ergebnis = Summe der Kind-Ergebnisse
            node['result'] = sum(child['result'] for child in childs)

    tree = appendChilds([n], delta, childsHandler)
    return tree

#print(dumps(fibonacci_demo(5), indent=2))