

def some_function(a, b):
    def adder():
        return a + b
    return adder

test = some_function(10, 2)
print(test)

result = test()
print(result)