from collections import defaultdict
import time


class NoObject:
    
    def __init__(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z):
        self.start = time.time()
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = a
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.m = m
        self.n = n
        self.o = o
        self.p = p
        self.q = q
        self.r = r
        self.s = s
        self.t = t
        self.u = u
        self.v = v
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        self.end = time.time()


class ObjectConfig(defaultdict):
    
    def __init__(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z):
        self.start = time.time()
        self['a'] = a
        self['b'] = b
        self['c'] = c
        self['d'] = d
        self['e'] = e
        self['f'] = f
        self['g'] = g
        self['h'] = a
        self['i'] = i
        self['j'] = j
        self['k'] = k
        self['l'] = l
        self['m'] = m
        self['n'] = n
        self['o'] = o
        self['p'] = p
        self['q'] = q
        self['r'] = r
        self['s'] = s
        self['t'] = t
        self['u'] = u
        self['v'] = v
        self['w'] = w
        self['x'] = x
        self['y'] = y
        self['z'] = z
        self.end = time.time()


class WithObject:
    
    def __init__(self, config: ObjectConfig):
        self.config = config
        self.start = time.time()
        for k, v in config.items():
            self.__setattr__(k, v)
        self.end = time.time()


def run_test():
    without_object = NoObject(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    config = ObjectConfig(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    with_object = WithObject(config)
    
    without_object2 = NoObject(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    config2 = ObjectConfig(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    with_object2 = WithObject(config2)

    avg_1 = []
    avg_2 = []
    avg_ovh1 = []
    avg_3 = []
    avg_4 = []
    avg_ovh2 = []

    for i in range(1000):
        diff_1 = round((without_object.end - without_object.start) * 1000000, 3)
        diff_2 = round((with_object.end - with_object.start) * 1000000, 3)
        overhead1 = diff_2 - diff_1
        avg_1.append(diff_1)
        avg_2.append(diff_2)
        avg_ovh1.append(overhead1)
    
    for i in range(1000):
        diff_3 = round((without_object2.end - without_object2.start) * 1000000, 3)
        diff_4 = round((with_object2.end - with_object2.start) * 1000000, 3)
        overhead2 = diff_4 - diff_3
        avg_3.append(diff_3)
        avg_4.append(diff_4)
        avg_ovh2.append(overhead2)
        
    for i in range(1000):
        diff_5 = round((with_object.config.end - with_object.config.start) * 100000, 3)
        diff_6 = round((with_object2.config.end - with_object2.config.start) * 100000, 3)

    def average_list(l):
        return sum(l) / len(l)

    result1 = round(average_list(avg_1), 3)    
    result2 = round(average_list(avg_2), 3)
    result3 = round(average_list(avg_3), 3)
    result4 = round(average_list(avg_4), 3)
    

    print("")
    print("All Float Arguments:")
    print("-------------------------------")
    print("Without config object: " + f"{result1}μs")
    print("With config object:    " + f"{result2}μs")
    print("Inefficiency:          " + f"{round(result2 / result1, 1)}x")
    print("")

    print("All Integer Arguments:")
    print("-------------------------------")
    print("Without config object: " + f"{result3}μs")
    print("With config object:    " + f"{result4}μs")
    print("Inefficiency:          " + f"{round(result4 / result3, 1)}x")
    print("")
    
    print("Type Adjusted:")
    print("-------------------------------")
    print("Without config object: " + f"{round(result1 - result3, 2)}μs")
    print("With config object:    " + f"{round(result2 - result4, 2)}μs")
    print("")
    
    # print("`defaultdict` init (`__setattr__` timing):")
    # print("-------------------------------")
    # print(f"Floats: {diff_5}μs  ({round(average_list(with_object.attr_time) * 1000000, 3)})")
    # print(f"Ints:   {diff_6}μs  ({round(average_list(with_object2.attr_time) * 1000000, 3)})")
    # print("")

"""
Discussion:
Interesting, so it appears in the balance that the vast majority of the time
wasted in the configuration object is just copying the attributes from the config
object to the target object.
"""

if __name__ == '__main__':
    run_test()