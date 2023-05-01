x = 5

def f() -> int:
    x = 3
    def g() -> int:
        return x
    return g()

print(f())