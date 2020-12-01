import numpy as np


test_array = np.array([
    [True, False],
    [False, True],
    [True, True],
    [False, False]
])


def function_to_apply(a):
    if a[0] == True:
        print(a)
    

np.apply_along_axis(function_to_apply, 0, test_array)

register = np.zeros(shape=(32, 16), dtype=np.int8)


def set_first_to_one(reg):
    reg[0] = 1
    return reg


register = np.apply_along_axis(set_first_to_one, 1, register)
print(register)