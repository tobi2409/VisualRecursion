from recursionlibrary import appendChilds, getObject

from json import dumps

def fak(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(childNodes, node):
        return node['value'] * childNodes[0]['value'] if len(childNodes) != 0 else 1

    def resultConditionCallback(childNodes, node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

fak(5)

def sum(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(childNodes, node):
        return node['value'] + childNodes[0]['value'] if len(childNodes) != 0 else node['value']

    def resultConditionCallback(childNodes, node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChilds([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

#sum(5)

def fib(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1, node['value'] - 2] if node['value'] - 1 >= 0 else []

    def combineCallback(childNodes, node):
        return childNodes[0]['value'] + childNodes[1]['value'] if len(childNodes) == 2 else 1

    def resultConditionCallback(childNodes, node):
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

#flatten([2, 5, 1, 7, [3, 8, [9, 0], 2], 6, 4])

#TODO: extend list, flatten list, binarysearch, mergesort