import time


def my_decorator(func, *args):
        print("Execution started:")
        tt1 = time.time()
        ret = func(*args)
        tt2 = time.time()
        print(func.__name__, "()")
        print("Execution done. Time: ", tt2-tt1)
        return ret


def myfunc():
    for i in range(0, 10000):
        i = i**2
    print("Print myfunc")


def transmogr(iterable, pred1, pred2=None, tran=None):
    iterable_new = []
    for val in iterable:
        if (pred1(val) is True):
            if pred2 is None:
                iterable_new.append(val)
                continue
            if pred2(val) is False:
                iterable_new.append(tran(val))
    return iterable_new


def is_even(val):
    if val % 2 == 0:
        return True
    return False


def my_map(tran, iterable):
    for ind in range(0, len(iterable)):
        iterable[ind] = tran(iterable[ind])
    return iterable


def my_filter(pred1, iterable):
    iterable_new = []
    for val in iterable:
        if (pred1(val) is True):
            iterable_new.append(val)
    return iterable_new


def my_reduce(func, iterable):
    ret = iterable[0]
    for i in range(1, len(iterable)):
        ret = func(iterable[i], ret)
    return ret


def mult2(val):
    return val*2


iterable = []
for i in range(1, 10):
    iterable.append(i)

print("My Filter: ", list(my_decorator(my_filter, is_even, iterable)))
print("Filter: ", list(my_decorator(filter, is_even, iterable)))
print("Decor: ", my_decorator(transmogr, iterable, is_even))
print("My Map: ", my_decorator(my_map, mult2, iterable))
print("Map: ", list(my_decorator(map, mult2, iterable)))
