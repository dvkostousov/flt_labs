# TRS T:
rules = [
    ("baaa","aaab"),
    ("aabb","abab"),
    ("aa","bab"),
    ("aaab","ab"),
    ("bbb","b"),
]

# TRS T' (правила, полученные из исходной trs после выполнения всего алгоритма Кнута-Бендикса):
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

# Мера M(w) = (A,B,C)
def measure(w):
    A = w.count('a')
    B = w.count('b')
    C = w.count("aa") + w.count("bb")
    n = len(w)
    s = 0
    for i,ch in enumerate(w, start=1):
        if ch == 'b':
            s += (n - i)
    C += s
    return (A, B, C)

# Сравнение слов u и v по M (A>B>C) + лексикографическое сравнение при равных M
def greater(u,v):
    mu = measure(u); mv = measure(v)
    if mu != mv:
        return mu > mv
    return u > v

# Редукция слова до НФ
def reduce_word(w, rules):
    while True:
        pos = None
        rule = None
        for r in rules:
            i = w.find(r[0])
            if i != -1:
                pos = i; rule = r
                break
        if rule is None:
            break
        w = w[:pos] + rule[1] + w[pos+len(rule[0]):]
    return w

# Генерация критических пар для пары (l1->r1, l2->r2)
def critical_pairs_from_pair(l1, r1, l2, r2):
    cps = []
    n1 = len(l1); n2 = len(l2)
    # 1) l2 встречается внутри l1
    for pos in range(0, max(0, n1 - n2) + 1):
        if l1[pos:pos+n2] == l2:
            w = l1
            s1 = r1
            s2 = l1[:pos] + r2 + l1[pos+n2:]
            cps.append((w, s1, s2))
    # 2) суффикс l1 совпадает с префиксом l2
    for k in range(1, min(n1, n2)):
        if l1[-k:] == l2[:k]:
            w = l1 + l2[k:]
            s1 = r1 + l2[k:]
            s2 = l1[:-k] + r2
            cps.append((w, s1, s2))
    return cps

# Алгоритм Кнута-Бендикса
def knuth_bendix(initial_rules):
    rules = initial_rules.copy()
    processed_pairs = set()
    iteration = 0
    added = True
    while added:
        iteration += 1
        added = False
        for i,ri in enumerate(rules):
            for j,rj in enumerate(rules):
                key = (ri[0], rj[0])
                if key in processed_pairs:
                    continue
                processed_pairs.add(key)
                cps = critical_pairs_from_pair(ri[0], ri[1], rj[0], rj[1])
                for (w, s1, s2) in cps:
                    red1 = reduce_word(s1, rules)
                    red2 = reduce_word(s2, rules)
                    if red1 == red2:
                        continue
                    if greater(red1, red2):
                        new_lhs, new_rhs = red1, red2
                    else:
                        new_lhs, new_rhs = red2, red1
                    if not any(r[0] == new_lhs and r[1] == new_rhs for r in rules):
                        rules.append((new_lhs, new_rhs))
                        added = True
    print(f"Итераций: {iteration - 1}\n")
    return rules

# Запуск
final_rules = knuth_bendix(rules)

# Для проверки итоговой trs:
# final_rules = knuth_bendix(new_rules)

print("Итоговая trs:")
for r in final_rules:
    print(f"{r[0]} -> {r[1]}")