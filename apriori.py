import itertools

def pruning(L,c):
    for sub in set(itertools.combinations(c, len(c)-1)):
        if sorted(list(sub)) not in L:
            return False
    return True

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

def GenerateC(L, k):
    candidates = []
    for i in range(0,len(L)):
        for j in range(i+1, len(L)):
            c = sorted(list(set(L[i]) | set(L[j])))
            if len(c) == len(L[i]) + 1:
                if pruning(L,c) and c not in candidates:
                        candidates.append(c)
    return candidates

def generateRules():
    rules = ""
    for pattern in filter(lambda x: len(x) > 1, frequentPatterns):
        for subset in getAllSubsets(pattern):
            diff = set(pattern) - set(subset)
            rules += makeRuleStr(list(subset),list(diff),getSupport(pattern),getConfidence(pattern,subset))
    return rules

def getAllSubsets(superSet):
    result = set()
    for i in range(1, len(superSet)):
        result = result | set(itertools.combinations(superSet, i))

    return result

def makeRuleStr(lhs, rhs, support, conf):
    return ("{%s}\t{%s}\t%.2f\t%.2f\n" % (",".join(map(str, lhs)), ",".join(map(str, rhs)), support, conf))

def roundTo2Dec(value):
    value = float(value)
    return round(value,2)


transactions = []
frequentPatterns = []
cache = {}
C = []
L = []

minSupport = 4

input_file = open("input.txt", 'r')
output_file = open("output.txt", "w")

lines = input_file.read().split('\n')

for line in lines:
    arr = list(map(int, line.split('\t')))
    C = list(set(C + arr))
    transactions.append(sorted(arr))
C = [[i] for i in C]

step = 2
while len(C) != 0:
    for item in C:
        support = getSupport(item)
        if support >= minSupport:
            L.append(item)
            if item not in frequentPatterns:
                frequentPatterns.append(item)
    C = GenerateC(L, step)
    step += 1
    L.clear()

output_file.write(generateRules())

input_file.close()
output_file.close()

