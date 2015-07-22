# permutations


def perm(s, r=None):
    if not s:
        return []
    n = len(s)
    r = n if (r > n or r == None) else r

    if n == 1 or r == 1:
        return list(s)

    result = []
    for i in range(n):
        result += [s[i]+item for item in perm(s[:i]+s[i+1:], r-1)]
    return result

s = 'asdf'

print perm('', 0)
print perm(s, 0)
print perm(s, 1)
print perm(s, 2)
print perm(s, 3)
print perm(s, 4)
print perm(s, 5)

import web
