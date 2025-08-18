def appendChilds(lst, filter, childsHandler=lambda childs, node: None):
    def factorNode(value, currentListIndex, lstSize, layer, childs, parent, history):
        return {'value': value, 'currentListIndex': currentListIndex, 'listSize': lstSize, 'layer': layer, 'childs': childs, 'parent': parent, 'history': history}

    def _appendChilds(lst, filter, layer=1, parent=None, history=[]):
        result = []

        nextLayer = layer + 1

        lstSize = len(lst)

        for i, e in enumerate(lst):
            node = factorNode(e, i, lstSize, layer, [], parent, history)

            filtered = filter(node, lst)
            if filtered != []:
                relationLessNode = factorNode(e, i, lstSize, layer, [], None, [])
                node['childs'].extend(_appendChilds(filtered, filter, layer=nextLayer, parent=relationLessNode, history=history))
                result.append(node)
                childsHandler(node['childs'], node) # childs-Input (u.a. für Sibling-Management des nächsten Layers) holen und Output in node eintragen

        return result

    root = factorNode(None, -1, -1, 0, [], None, [])
    root['childs'].extend(_appendChilds(lst, filter, history=[]))
    return root

from json import dumps

def demo1():
    def filter(node, lst):
        return lst if node['layer'] <= 2 else []

    print(dumps(appendChilds([8,6,3,7], filter), indent=2))

#demo1()

def demo2():
    def filter(node, lst):
        return lst if node['layer'] <= 2 and (node['parent'] is None or node['value'] != node['parent']['value']) else []

    print(dumps(appendChilds([8,6,3], filter), indent=2))

demo2()