import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChilds, getObject

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

fak(5)