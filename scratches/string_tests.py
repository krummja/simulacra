

string = "aaaaaaaaaa"  # len = 10
print(len(string))

def some_decorator(string):
    return string

string2 = f"{some_decorator('aaaaa')}{string}"
print(len(string2))