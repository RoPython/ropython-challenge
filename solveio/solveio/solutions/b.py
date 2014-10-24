# Se da o lista cu siruri. Sa se elimine din acea lista,
# toate sirurile ce au in acelasi timp un numar par de caractere
# si care contin cel putin o litera ce se repeta de doua sau
# de mai multe ori.
#
# Precizari:
#    - listele au cel putin un element
#    - raspunsul trebuie ordonat
#    - litere mici ale alfabetului englez


# ------------

from random import randint, sample

alpha = [chr(nr) for nr in range(ord("a"), ord("z") + 1)] 

def generate():
    for _ in range(10):
        data = []
        dlen = randint(1, 5)
        for _ in range(dlen):
            slen = randint(1, 20)
            slist = []
            for _ in range(slen):
                slist.extend(sample(alpha, 1))
            data.append("".join(slist))
        yield data

# ------------


def compute(data):
    for x in data[:]:    # pentru fiecare sir din lista
        if len(x) % 2 == 0:
            # avem numar par de caractere
            for c in x:    # pentru fiecare caracter din sir
                if x.count(c) > 1:
                    # avem mai mult de o aparitie
                    # deci avem ambele conditii valabile
                    data.remove(x)
                    # sirul a fost sters, nu ne mai intereseaza
                    # si alte verificari in privinta lui
                    break    # intrerupem fortat bucla
    # intoarcem noul `data`
    data.sort()
    return data


if __name__ == "__main__":
    assert compute(["defg", "abc"]) == ["abc", "defg"]
    assert compute(["afaf", "defgee"]) == []
    assert compute(["aaaaa"]) == ["aaaaa"]
