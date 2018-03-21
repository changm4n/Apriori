import itertools

def pruning(L,c):
    for sub in set(itertools.combinations(c, len(c)-1)):
        if sorted(list(sub)) not in L:
            return False
    return True

def getSupport(item):
    support = 0
    for transaction in transactions:
        if set(item).issubset(set(transaction)):
            support += 1
    return support


def GenerateC(L, k):
    candidates = []
    for i in range(0,len(L)):
        for j in range(i+1, len(L)):
            L1 = L[i][:k-2]
            L2 = L[j][:k-2]
            if L1 == L2:
                c = set(L[i]) | set(L[j])
                if pruning(L,c):
                    candidates.append(list(c))

    return candidates

transactions = []
frequentPatterns = []
C = []
L = []

minSupport = 2

####Input####
f = open("input.txt", 'r')
lines = f.read().split('\n')
f.close()
for line in lines:
    arr = list(map(int, line.split(' ')))
    C = list(set(C + arr))
    transactions.append(sorted(arr))
C = [[i] for i in C]
###############


####Apriori####
while len(C) != 0:
    for item in C:
        if getSupport(item) >= minSupport:
            L.append(item)
            frequentPatterns.append(item)

    C = GenerateC(L, len(L[0]) + 1)
    L.clear()
###############

print(frequentPatterns)




