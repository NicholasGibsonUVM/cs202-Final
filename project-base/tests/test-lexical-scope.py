x = 5

def f() -> Callable[[], int]:
    def g() -> int:
        return x
    return g

print(f()())