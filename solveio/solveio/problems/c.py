# Se da un dictionar ca intrare. Functia trebuie sa intoarca
# o multime ce reprezinta intersectia multimii cheilor cu
# multimea valorilor. Multimea intoarsa trebuie sa fie sub
# forma unei liste ordonate.


def compute(data):
    pass


if __name__ == "__main__":
    assert compute({"1": "2", "2": "1"}) == {"1", "2"}
    assert compute({"1": "1", "2": "3"}) == {"1"}
    assert compute({"1": "2", "3": "4", "5": "6"}) == {}
