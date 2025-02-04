
# if-elif-else
# loops
# functions
# datetime
# list, tuple, set, dict

from datetime import datetime, timedelta

print(datetime.now())
print(datetime(2024, 2, 20, 14, 30, 2, 200))

diff = datetime.now() - datetime(2024, 12, 31, 23, 59, 59, 9999)
print(diff.seconds)
print(datetime.now() + timedelta(days=32))

# list -- can do all operations: add, remove, index
# tuple -- read-only
# dict -- key: value
# set -- no duplications , no order
print([4, -2, 3, 0, 5], 'filter', list(filter(lambda x: x > 0, [4, -2, 3, 0, 5] )))
print([4, -2, 3, 0, 5], 'map', list(map(lambda x: x ** 2, [4, -2, 3, 0, 5])))
print(sorted(['aaa', 'bc','', 'a', 'z', 'ddddd'], key= lambda w: len(w)))
#           3     2  0    1   1       5
#           0 1 1 2 3 5
print(set([4, 5, 3, 4, 4, 5, 5, 1]))
print({ 'id': 1, 'name': 'dana', 'age': 39})