x = 5

def f():
    x = 3
    def g():
        print(x)
    return g

print(f()())