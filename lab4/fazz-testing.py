import time
import random
import matplotlib.pyplot as plt
import numpy as np

def parse_T_naive(s, l, r):
    vals = set()
    # T -> bb
    if r - l == 2 and s[l:r] == "bb":
        vals.add(1)
    # T -> T a T
    for k in range(l + 1, r - 1):
        if s[k] == 'a':
            left = parse_T_naive(s, l, k)
            right = parse_T_naive(s, k + 1, r)
            for a in left:
                for b in right:
                    vals.add(a + b)
    return vals

def parse_S_naive(s, l, r):
    vals = set()
    # S -> aba
    if r - l == 3 and s[l:r] == "aba":
        vals.add(1)
    # S -> bb S
    if r - l >= 2 and s[l:l+2] == "bb":
        inner = parse_S_naive(s, l+2, r)
        if inner:
            vals.add(0)
    # S -> T a S S a T  условие S1.v == S2.v, S0.v := min(T1.v, T2.v)
    for i in range(l + 1, r):
        if s[i] != 'a':
            continue
        for j in range(i + 1, r):
            for k in range(j + 1, r):
                if s[k] != 'a':
                    continue
                T1 = parse_T_naive(s, l, i)
                if not T1:
                    continue
                S1 = parse_S_naive(s, i+1, j)
                if not S1:
                    continue
                S2 = parse_S_naive(s, j, k)
                if not S2:
                    continue
                T2 = parse_T_naive(s, k+1, r)
                if not T2:
                    continue
                for v1 in S1:
                    for v2 in S2:
                        if v1 == v2:
                            for t1 in T1:
                                for t2 in T2:
                                    vals.add(min(t1, t2))
    return vals

def in_language_naive(s):
    return bool(parse_S_naive(s, 0, len(s)))

def optimized_parse(s):
    n = len(s)

    # T -> bb (abb)^k , T.v = k + 1
    def T_value(l, r):
        if r - l < 2 or s[l:l+2] != "bb":
            return None
        i = l + 2
        k = 0
        while i < r:
            if i + 3 > r or s[i:i+3] != "abb":
                return None
            i += 3
            k += 1
        return k + 1

    S_vals = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # S -> aba
    for i in range(n - 2):
        if s[i:i+3] == "aba":
            S_vals[i][i+3].add(1)

    # перебор длины
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length

            # S -> bb S
            if r - l >= 4 and s[l:l+2] == "bb":
                if S_vals[l+2][r]:
                    S_vals[l][r].add(0)

            # S -> T a S S a T
            for i in range(l + 2, r - 3):
                if s[i] != 'a':
                    continue

                T1 = T_value(l, i)
                if T1 is None:
                    continue

                for k in range(i + 3, r - 1):
                    if s[k] != 'a':
                        continue

                    T2 = T_value(k + 1, r)
                    if T2 is None:
                        continue

                    # S S между i и k
                    for j in range(i + 1, k):
                        if not S_vals[i+1][j] or not S_vals[j][k]:
                            continue

                        # пересечение значений
                        if S_vals[i+1][j] & S_vals[j][k]:
                            S_vals[l][r].add(min(T1, T2))

    return S_vals[0][n]

def in_language_optimized(s):
    return bool(optimized_parse(s))

def gen_S(level=0, v=-1):
    if level == 2:
        return "aba", 1
    case = random.randint(1, 100)
    if case <= 40 and (v == -1 or v == 0):
        w, _ = gen_S(level=level + 1)
        return "bb" * random.randint(1, 3) + w, 0
    if 40 <= case <= 80 and (v == -1 or v == 1):
        return "aba", 1
    res = ""
    if v != -1 and v != 0:
        v3, v4 = v, v + 1
    else:
        v3, v4 = random.randint(1, 3), random.randint(1, 3)
    S1, v1 = gen_S(level=level + 1)
    S2, _ = gen_S(level=level + 1, v=v1)
    if v == 0:
        res += "bb" * random.randint(1, 3)
    return res + "bba" * v3 + S1 + S2 + "abb" * v4, min(v3, v4) * (v != 0)

def generate_positive_set(n):
    res = set()
    while len(res) < n:
        w, _ = gen_S()
        if len(w) <= 40:
            res.add(w)
    return list(res)

def generate_random_word(length):
    return ''.join(random.choice(['a', 'b']) for i in range(length))

def generate_negative_set(n, min_l, max_l):
    res = set()
    while len(res) < n:
        w = generate_random_word(random.randint(min_l, max_l))
        if not in_language_optimized(w):
            res.add(w)
    return list(res)

def run_benchmark(words):
    results = []
    for w in words:
        rec = {'word': w, 'len': len(w)}

        t0 = time.perf_counter()
        try:
            res_naive = in_language_naive(w)
        except RecursionError:
            res_naive = None
        t1 = time.perf_counter()
        rec['naive_res'] = res_naive
        rec['naive_time_ms'] = (t1 - t0) * 1000.0
        t0 = time.perf_counter()
        res_opt = in_language_optimized(w)
        t1 = time.perf_counter()
        rec['opt_res'] = res_opt
        rec['opt_time_ms'] = (t1 - t0) * 1000.0

        rec['match'] = (rec['naive_res'] == rec['opt_res'])

        results.append(rec)
        print(f"Длина = {rec['len']} | наивный = {rec['naive_res']} ({rec['naive_time_ms']:.1f} мс) | "
              f"оптимизированный = {rec['opt_res']} ({rec['opt_time_ms']:.1f} мс) | совпадение = {rec['match']} | слово = {w}")

    naive_times = [r['naive_time_ms'] for r in results if r['naive_time_ms'] is not None]
    opt_times = [r['opt_time_ms'] for r in results if r['opt_time_ms'] is not None]
    print("\nИтого:")
    if naive_times:
        print(f" Наивный: {sum(naive_times):.1f} мс, среднее: {sum(naive_times)/len(naive_times):.1f} мс")
    if opt_times:
        print(f" Оптимизированный: {sum(opt_times):.1f} мс, среднее {sum(opt_times)/len(opt_times):.1f} мс")
    matches = [r['match'] for r in results if r['match'] is not None]
    if matches:
        print(f" Совпадений: {sum(1 for m in matches if m):d}/{len(matches)}")

    return results


def plot_benchmark(results, title):
    grouped = {}
    for r in results:
        length = r['len']
        if length not in grouped:
            grouped[length] = []
        grouped[length].append(r)

    lengths_sorted = sorted(grouped.keys())
    avg_naive_times = []
    avg_opt_times = []

    for length in lengths_sorted:
        group = grouped[length]
        naive_times = [r['naive_time_ms'] for r in group]
        opt_times = [r['opt_time_ms'] for r in group]
        avg_naive_times.append(np.mean(naive_times))
        avg_opt_times.append(np.mean(opt_times))

    plt.figure(figsize=(10, 6))

    for r in results:
        plt.scatter(r['len'], r['naive_time_ms'], color='red', alpha=0.3)
        plt.scatter(r['len'], r['opt_time_ms'], color='green', alpha=0.3)

    plt.plot(lengths_sorted, avg_naive_times, color='red', label='Наивный (среднее)', linewidth=2)
    plt.plot(lengths_sorted, avg_opt_times, color='green', label='Оптимизированный (среднее)', linewidth=2)

    plt.xlabel("Длина слова")
    plt.ylabel("Время работы (мс)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

#random.seed(123)
print("\nБатч слов из языка")
positive_results = run_benchmark(generate_positive_set(10))
print("\nБатч слов не из языка")
negative_results = run_benchmark(generate_negative_set(10, 10, 30))

plot_benchmark(positive_results, "Сравнение скорости: слова из языка")
plot_benchmark(negative_results, "Сравнение скорости: слова не из языка")
