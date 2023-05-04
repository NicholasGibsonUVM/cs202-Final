x = 5

def f() -> int:
    return x

x = 6

def g(a: int) -> int:
    y = 20
    anonymous: Callable[[int], int] = lambda z: x + y + z + a
    y = 0
    a = 3
    return anonymous(a)

print(f())
print(g(2))