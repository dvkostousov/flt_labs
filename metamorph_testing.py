import re
from random import randint, choice, seed

# TRS T':
rules = [
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

# Проверка на сохранение инвариантов
# Инварианты:
# 1) количество символов a (монотонно уменьшается, либо не изменяется)
# 2) четность количества букв b (не изменяется)
def check(old_w, new_w):
    return old_w.count('b') % 2 == new_w.count('b') % 2 and old_w.count('a') >= new_w.count('a')

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

    w1 = reduce_word(w, rules)
    f = True
    while w1 != w:
        if not check(w, w1):
            f = False
            break
        w1, w = reduce_word(w1, rules), w1
    print(f"Итоговое слово: {w1}")
    if f:
        print("Выполнимость инвариантов подтверждена")
    else:
        print("Выполнимость инвариантов НЕ подтверждена")
    print()
    ff.append(f)

if all(ff):
    print("Системы эквивалентны по метаморфному тестированию")
else:
    print("Системы НЕ эквивалентны по метаморфному тестированию")