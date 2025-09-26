import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChilds, getObject

from json import dumps

def mergeSort(lst):
    def delta(node, lst, originalLst):
        if len(node['value']) <= 1:
            return []

        mid = len(node['value']) // 2
        return [node['value'][:mid], node['value'][mid:]]

    def combineChildNodesCallback(node, childNodes):
        if len(childNodes) == 0:
            return node['value']

        left, right = childNodes[0]['value'], childNodes[1]['value']
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
        combineChildNodesCallback=combineChildNodesCallback,
        resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True), indent=2))

mergeSort([7, 3, 8, 4, 2, 1, 9, 5])