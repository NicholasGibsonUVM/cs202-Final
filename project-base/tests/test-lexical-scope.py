x = 5

def f() -> int:
    def g() -> int:
        return x
    return g()

print(f())