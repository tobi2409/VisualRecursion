from recursionlibrary import appendChilds, divideAndConquer, getObject

from json import dumps

def fak(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(node):
        return node['value'] * node['childs'][0]['value'] if len(node['childs']) != 0 else 1

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

#fak(5)

def sum(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(node):
        return node['value'] + node['childs'][0]['value'] if len(node['childs']) != 0 else node['value']

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

#sum(5)

def fib(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1, node['value'] - 2] if node['value'] - 1 >= 0 else []

    def combineCallback(node):
        return node['childs'][0]['value'] + node['childs'][1]['value'] if len(node['childs']) == 2 else 1

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

#fib(7)

"""
Angenommen, ein Kind kann eine Treppe mit s Stufen erklimmen, indem es entweder 1, 2, ..., k
Stufen in einem einzigen Schritt nimmt. Berechnen Sie alle unterschiedlichen Schrittfolgen, mit
denen das Kind genau die s Stufen der Treppe erklimmt.
"""

#TODO: Parents müssen noch dereferenziert werden
def steps(s):
    def delta(node, lst, originalLst):
        return [i for i in range(1, s + 1)] if node['value'] <= s else []

    def bufferCallback(node):
        return node['value'] + (getObject(node['parent'])['value'] if node['parent'] != None else 0)
        
    print(dumps(appendChilds([i for i in range(1, s + 1)], delta, bufferCallback=bufferCallback), indent=2))

#steps(5)

def fullExpansion():
    def delta(node, lst, originalLst):
        return lst if node['layer'] <= 2 else []

    def resultNodeCallback(node):
        return None

    print(dumps(appendChilds([8,6,3,7], delta, resultNodeCallback=resultNodeCallback), indent=2))

#fullExpansion()

def distinctExpansion():
    def delta(node, lst, originalLst):
        return [e for e in lst if e != node['value']]

    def resultNodeCallback(node):
        return None

    print(dumps(appendChilds([8,6,3,7], delta, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True), indent=2))

#distinctExpansion()

def flatten(lst):
    def delta(node, lst, originalLst):
        # klar kann man das auch in einem Einzeiler schreiben, aber es soll veranschaulicht werden, dass auch ein normales int als delta ausgegeben werden kann
        # -> in dem Fall findet einfach keine weitere Rekursion mehr statt und das int wird zum Blatt
        if type(node['value']) == list:
            return node['value']
        elif type(node['value']) == int:
            return node['value']

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds(lst, delta, resultNodeCallback=resultNodeCallback), indent=2))

#flatten([2, 5, 1, 7, [3, 8, [9, [4, 1], 0], 2], 6, 4])

def mergeSort1(lst):
    def delta(node, lst, originalLst):
        if len(node['value']) <= 1:
            return []

        mid = len(node['value']) // 2
        return [node['value'][:mid], node['value'][mid:]]

    def combineCallback(node):
        if len(node['childs']) == 0:
            return node['value']

        left, right = node['childs'][0]['value'], node['childs'][1]['value']
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([lst], delta,
        combineCallback=combineCallback,
        resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True), indent=2))

#mergeSort1([7, 3, 8, 4, 2, 1, 9, 5])

# Divide-And-Conquer-API ist eher ungünstig, da es ziemlich viele Klassifikationen von Divide-And-Conquer-Algorithmen gibt
# besser ist vielleicht in appendChilds ein mergeChildsCallback zu integrieren
# oder eben gleich eine neue Schicht aufbauen, welche zum WYSIWYG-Editor rüberleitet
def mergeSort2(lst):
    def mergeChildsCallback(childs, node):
        merged = []

        i = j = 0
        while i < len(childs[0]['value']) and j < len(childs[1]['value']):
            if childs[0]['value'][i] < childs[1]['value'][j]:
                merged.append(childs[0]['value'][i])
                i += 1
            else:
                merged.append(childs[1]['value'][j])
                j += 1

        merged.extend(childs[0]['value'][i:])
        merged.extend(childs[1]['value'][j:])

        return merged

    def resultNodeCallback(node):
        return node['value']

    print(dumps(divideAndConquer(lst, mergeChildsCallback=mergeChildsCallback, resultNodeCallback=resultNodeCallback), indent=2))

#mergeSort2([7, 3, 8, 4, 2, 1, 9, 5])

#TODO: binarysearch