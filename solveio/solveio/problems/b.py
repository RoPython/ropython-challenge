# Se da o lista cu siruri. Sa se elimine din acea lista,
# toate sirurile ce au in acelasi timp un numar par de caractere
# si care contin cel putin o litera ce se repeta de doua sau
# de mai multe ori.
#
# Precizari:
#    - listele au cel putin un element
#    - raspunsul trebuie ordonat
#    - litere mici ale alfabetului englez


def compute(data):
    pass


if __name__ == "__main__":
    assert compute(["defg", "abc"]) == ["abc", "defg"]
    assert compute(["afaf", "defgee"]) == []
    assert compute(["aaaaa"]) == ["aaaaa"]
