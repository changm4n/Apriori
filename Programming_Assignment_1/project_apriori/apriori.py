from utils import *
import sys

def getSupport(item):
    itemSet = frozenset(item)
    if itemSet in cache:
        return cache[itemSet]
    else:
        count = 0
        for transaction in transactions:
            if set(item).issubset(set(transaction)):
                count += 1
        support = roundTo2Dec(count / len(transactions) * 100)
        cache[itemSet] = support
        return support

def getConfidence(lhs, rhs):
    return roundTo2Dec(getSupport(lhs) / getSupport(rhs) * 100)

def GenerateC(Ln):
    candidates = []
    for i in range(0,len(Ln)):
        for j in range(i+1, len(Ln)):
            c = sorted(list(set(Ln[i]) | set(Ln[j])))
            if len(c) == len(Ln[i]) + 1:
                if pruning(Ln,c) and c not in candidates:
                        candidates.append(c)
    return candidates

def pruning(Ln,c):
    for sub in set(getSubsets(c, len(c)-1)):
        if sorted(list(sub)) not in Ln:
            return False
    return True

def generateRules():
    rules = ""
    for pattern in filter(lambda x: len(x) > 1, frequentPatterns):
        for subset in getAllSubsets(pattern):
            rest = set(pattern) - set(subset)
            rules += makeRuleStr(list(subset),list(rest),getSupport(pattern),getConfidence(pattern,subset))
    return rules

transactions = []
frequentPatterns = []
cache = {}
C = []
L = []

if len(sys.argv) != 4:
    print("invalid argument")
    sys.exit()

minSupport = int(sys.argv[1])
input_file = open(sys.argv[2], 'r')
output_file = open(sys.argv[3], "w")

lines = input_file.read().split('\n')

for line in lines:
    arr = list(map(int, line.split('\t')))
    C = list(set(C + arr))
    transactions.append(sorted(arr))
C = [[i] for i in C]

while len(C) != 0:
    for item in C:
        support = getSupport(item)
        if support >= minSupport:
            L.append(item)
            if item not in frequentPatterns:
                frequentPatterns.append(item)
    C = GenerateC(L)
    L.clear()

output_file.write(generateRules())

input_file.close()
output_file.close()
