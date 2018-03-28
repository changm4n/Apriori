import itertools
from decimal import Decimal, ROUND_HALF_UP

def getAllSubsets(superSet):
    result = set()
    for i in range(1, len(superSet)):
        result = result | set(itertools.combinations(superSet, i))

    return result

def roundTo2Dec(value):
    return Decimal(str(value)).quantize(Decimal('0.01'), 
    rounding= ROUND_HALF_UP)

def getSubsets(superSet, length):
    return set(itertools.combinations(superSet, length))

def makeRuleStr(lhs, rhs, support, conf):
    return ("{%s}\t{%s}\t%0.2f\t%0.2f\n" % (",".join(map(str, lhs)), ",".join(map(str, rhs)), support, conf))