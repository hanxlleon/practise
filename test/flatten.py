#coding: utf-8
# 展开嵌套序列


def is_list_or_tuple(x):
    return isinstance(x, (list, tuple))


def flatten(seq, to_expand=is_list_or_tuple):
    for item in seq:
        if to_expand(item):
            for subitem in flatten(item, to_expand):
                yield subitem
        else:
            yield item


# python 3
# def flatten(seq, to_expand=is_list_or_tuple):
#     for item in seq:
#         if to_expand(item):
#             yield from flatten(item, to_expand)
#
#         else:
#             yield item


s = [2, 3, [4, 5, 6, [4, 5, [7, 8], []], (2, 3, 4)], ['s', 'sd'], (4, 5)]

for i in flatten(s):
    print i
