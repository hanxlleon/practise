def substring(s1, s2):

    start, end = 0, 0
    for i in range(len(s1)):
        k = i
        s, e = -1, 0
        for j in range(len(s2)):
            if k > len(s1)-1:
                break
            if s1[k] == s2[j]:
                s = k if s == -1 else s
                e = k
                (start, end) = (s, e) if end-start < e - s else (start, end)
            else:
                k = i
                s, e = -1, 0

            k += 1

    return start, end, s1[start:end+1]


print substring('123asdfghjklklsdf1212312', 'asdsdf1dasdfghjkl1')
