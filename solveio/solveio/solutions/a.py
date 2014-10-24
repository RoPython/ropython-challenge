# Sa se calculeze suma numerelor din lista primita ca intrare,
# dar si media aritmetica si geometrica a acestora.
# Sa se returneze o lista cu aceste rezultate
# in ordinea precizata mai sus.
# Numerele sunt naturale si nenule, iar lista de intrare are
# cel putin un element.
#
# Sugestii:
#    - folositi functia `round` pentru a pastra doar primele doua zecimale


# ----------

from random import randint

def generate():
    for _ in range(10):
        data = list()
        for _ in range(randint(1, 10)):
            data.append(randint(1, 100))
        yield data

# ----------


def compute(data):
    # obtinem marimea listei
    cnt = len(data)
    # calculam suma
    dsum = sum(data)
    # obtinem media aritmetica
    arit = dsum / cnt
    # si media geometrica
    geom = 1
    for nr in data:
        geom *= nr
    geom = pow(geom, 1 / cnt)
    # intoarcem rezultatul rotunjit
    return [dsum, round(arit, 2), round(geom, 2)]


if __name__ == "__main__":
    assert compute([1, 2, 3]) == [6, 2, 1.82]
    assert compute([2, 8]) == [10, 5, 4]
    assert compute([1, 1, 1, 1]) == [4, 1, 1]
