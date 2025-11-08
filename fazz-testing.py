import re
from random import randint, choice, seed

# TRS T:
rules = [
    ("baaa","aaab"),
    ("aabb","abab"),
    ("aa","bab"),
    ("aaab","ab"),
    ("bbb","b"),
]

# TRS T':
new_rules = [
    ("baaa", "aaab"),
    ("aabb", "abab"),
    ("aa", "bab"),
    ("aaab", "ab"),
    ("bbb", "b"),
    ("babbabab", "babababb"),
    ("bbabbab", "babbabb"),
    ("bbaba", "babab"),
    ("bababa", "babbabb"),
    ("bababbabb", "babbab"),
    ("babbab", "bbabb"),
    ("bbabb", "bab"),
    ("abab", "bab"),
    ("abbab", "bbab"),
    ("baba", "bab"),
    ("bbab", "babb"),
    ("bab", "abb"),
    ("aba", "ab"),
    ("abba", "abb")
]

# Редукция слова на 1 итерацию (правило выбирается случайным образом)
def reduce_word(w, rules):
    app_rules = []
    for r in rules:
        if r[0] in w:
            app_rules.append((r, choice([i.start() for i in re.finditer(r[0], w)])))

    if len(app_rules) == 0:
        return w
    rule, pos = choice(app_rules)
    return w[:pos] + rule[1] + w[pos+len(rule[0]):]

# Основная функция - проверка на достижимость из изначального слова в итоговое по правилам TRS
def check(old_w, new_w, rules):
    words = {old_w}
    normal_forms = set()
    while len(words) != 0 and new_w not in words:
        new_words = set()
        for w in words:
            f = True
            for r in rules:
                if r[0] in w:
                    f = False
                    for match in re.finditer(r[0], w):
                        new_words.add(w[:match.start()] + r[1] + w[match.end():])
            if f:
                normal_forms.add(w)
        words = new_words.difference(normal_forms)

    return new_w in words

# Запуск
seed(1312312312)

# Количество слов для проверки
n_w = 100

ff = []
for i in range(n_w):
    # Длина одного слова
    l_w = randint(10, 100)

    # Случайное слово
    w = ''.join([choice(["a", "b"]) for i in range(l_w)])
    print(f"Изначальное слово: {w}")

    # Максимальное количество итераций редукции
    max_iterations = 10

    iteration = 0
    w1 = reduce_word(w, rules)
    while iteration < max_iterations and w1 != w:
        if w1 == w:
            break
        iteration += 1
        w1, w = reduce_word(w1, rules), w1
    print(f"Итоговое слово: {w1}")

    f = check(w, w1, new_rules)
    ff.append(f)
    if f:
        print("Итоговое слово можно получить из изначального по правилам T'")
    else:
        print("Итоговое слово нельзя получить из изначального по правилам T'")
    print()

if all(ff):
    print("Системы эквивалентны по фазз-тестированию")
else:
    print("Системы НЕ эквивалентны по фазз-тестированию")
