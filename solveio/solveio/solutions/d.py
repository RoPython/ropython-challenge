# Se da un numar natural mai mare ca 10 si mai mic decat 100
# ca date de intrare. Sa se determine toate numerele prime
# mai mici strict decat numarul dat, apoi sa fie transformate
# intr-un sir de caractere in ordine inversa si in final,
# aceste siruri sa fie stocate intr-o lista ordonata.


# ----------

from random import randint

def generate():
    for _ in range(10):
        yield randint(11, 99)

# ----------


from math import sqrt


def prim(nr):
    if nr == 2:
        return True
    if not nr % 2:
        return False
    for i in range(3, int(sqrt(nr)) + 1, 2):
        if not nr % i:
            return False
    return True


def compute(data):
    ret = []
    for nr in range(2, data):
        if prim(nr):
            ret.append("".join(reversed(str(nr))))
    ret.sort()
    return ret


if __name__ == "__main__":
    assert compute(11) == ["2", "3", "5", "7"]
    assert compute(14) == ["11", "2", "3", "31", "5", "7"]
    assert compute(20) == ["11", "2", "3", "31", "5", "7", "71", "91"]
