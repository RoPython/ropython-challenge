# Se da un dictionar ca intrare. Functia trebuie sa intoarca
# o multime ce reprezinta intersectia multimii cheilor cu
# multimea valorilor. Multimea intoarsa trebuie sa fie sub
# forma unei liste ordonate.


# ----------

from random import randint

def generate():
    for _ in range(10):
        data = {}
        for _ in range(randint(1, 10)):
            k, v = str(randint(1, 20)), str(randint(1, 20))
            data[k] = v
        yield data

# ----------


def compute(data):
    # multimea cheilor
    a = set(data.keys())
    # si a valorilor
    b = set(data.values())
    # intoarcem intersectia
    r = a.intersection(b)
    return sorted(r)


if __name__ == "__main__":
    assert compute({"1": "2", "2": "1"}) == ["1", "2"]
    assert compute({"1": "1", "2": "3"}) == ["1"]
    assert compute({"1": "2", "3": "4", "5": "6"}) == []
