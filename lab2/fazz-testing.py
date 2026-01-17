import random
import re

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        s = stack.pop()
        for nxt in transitions.get(s, {}).get("ε", set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


class NFA:
    def __init__(self, transitions, start_states, final_states):
        self.transitions = transitions
        self.start_states = start_states
        self.final_states = final_states

    def accepts(self, word):
        current = epsilon_closure(self.start_states, self.transitions)

        for symbol in word:
            next_states = set()
            for s in current:
                next_states |= self.transitions.get(s, {}).get(symbol, set())

            if not next_states:
                return False

            current = epsilon_closure(next_states, self.transitions)

        return bool(current & self.final_states)

class DFA:
    def __init__(self, transitions, start_state, final_states):
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def accepts(self, word):
        state = self.start_state
        for symbol in word:
            if symbol not in self.transitions.get(state, {}):
                return False
            state = self.transitions[state][symbol]
        return state in self.final_states

# вспомогательный класс для ПКА
class SubAutomaton:
    def __init__(self, state):
        self.state = state


class AFA:
    def __init__(self, transitions, final_states):
        self.transitions = transitions
        self.final_states = final_states

    def accepts(self, word):
        # старт: основной (минимальный ДКА) + два подавтомата по глобальным инвариантам
        automata = [
            SubAutomaton("q1"),
            SubAutomaton("q24"),
            SubAutomaton("q27"),
        ]

        for symbol in word:
            next_automata = []

            for a in automata:
                state = a.state

                if symbol not in self.transitions.get(state, {}):
                    return False

                target = self.transitions[state][symbol]

                if target == "&1":
                    next_automata.append(SubAutomaton("&1"))
                    # новый подавтомат для локального инварианта
                    next_automata.append(SubAutomaton("q29"))
                else:
                    next_automata.append(SubAutomaton(target))

            automata = []
            for a in next_automata:
                if a.state == "&1":
                    automata.append(SubAutomaton("q9"))
                    automata.append(SubAutomaton("q29"))
                else:
                    automata.append(a)

        return all(a.state in self.final_states for a in automata)


# проверка по регулярному выражению
def check_regex(word):
    return bool(re.fullmatch(REGEX, word))


# генерация случайных слов
def generate_words(alphabet, min_len, max_len, batch_size):
    return [
        ''.join(random.choice(alphabet) for _ in range(random.randint(min_len, max_len)))
        for _ in range(batch_size)
    ]


NFA_TRANSITIONS = {
    "q1": {"a": {"q2"}, "ε": {"q4"}},
    "q2": {"b": {"q3"}},

    "q4": {"b": {"q5", "q7", "q15"}, "a": {"q6", "q8", "q12"}},
    "q5": {"b": {"q4"}},
    "q6": {"a": {"q4"}},

    "q7": {"b": {"q7"}},

    "q8": {"a": {"q9"}, "b": {"q9", "q10"}},
    "q9": {"c": {"q8"}},

    "q10": {"a": {"q11"}},
    "q11": {"a": {"q18"}},
    "q12": {"b": {"q13"}},
    "q13": {"c": {"q14"}},
    "q14": {"a": {"q12"}, "b": {"q15"}},

    "q15": {"c": {"q16"}},
    "q16": {"a": {"q14"}},
}

NFA_START = {"q1"}
NFA_FINAL = {"q3", "q4", "q7", "q18", "q12"}

DFA_TRANSITIONS = {
    "q1": {"a": "q2", "b": "q3"},
    "q2": {"a": "q4", "b": "q5"},
    "q3": {"b": "q6", "c": "q7"},
    "q4": {"a": "q8", "b": "q3", "c": "q9"},
    "q5": {"a": "q10", "c": "q11"},
    "q6": {"a": "q8", "b": "q3"},
    "q7": {"a": "q12"},
    "q8": {"a": "q4", "b": "q13"},
    "q9": {"a": "q14", "b": "q15"},
    "q10": {"a": "q16"},
    "q11": {"a": "q17", "b": "q18"},
    "q12": {"a": "q19", "b": "q20"},
    "q13": {"a": "q10", "c": "q11"},
    "q14": {"c": "q9"},
    "q15": {"a": "q10", "c": "q9"},
    "q17": {"b": "q21", "c": "q9"},
    "q18": {"a": "q10", "c": "q22"},
    "q19": {"b": "q21"},
    "q20": {"c": "q7"},
    "q21": {"c": "q12"},
    "q22": {"a": "q23", "b": "q15"},
    "q23": {"a": "q19", "b": "q20", "c": "q9"},
}

DFA_START = "q1"
DFA_FINAL = {"q1", "q2", "q3", "q4", "q5", "q6", "q8", "q16", "q17", "q19"}

AFA_TRANSITIONS = {
    "q24": {"a": "q24", "b": "q24", "c": "q25"},
    "q25": {"a": "q24", "b": "q24", "c": "q26"},

    "q27": {"a": "q27", "b": "q27", "c": "q28"},
    "q28": {"a": "q27", "b": "q27", "c": "q28"},

    "q29": {"a": "q30", "b": "q30", "c": "q30"},
    "q30": {"a": "q29", "b": "q29", "c": "q29"},

    "q1": {"a": "q2", "b": "q3"},
    "q2": {"a": "q4", "b": "q5"},
    "q3": {"b": "q6", "c": "q7"},
    "q4": {"a": "q8", "b": "q3", "c": "&1"},
    "q5": {"a": "q10", "c": "q11"},
    "q6": {"a": "q8", "b": "q3"},
    "q7": {"a": "q12"},
    "q8": {"a": "q4", "b": "q13"},

    "q9": {"a": "q14", "b": "q15"},
    "q10": {"a": "q16"},
    "q11": {"a": "q17", "b": "q18"},
    "q12": {"a": "q19", "b": "q20"},
    "q13": {"a": "q10", "c": "q11"},

    "q14": {"c": "&1"},
    "q15": {"a": "q10", "c": "&1"},
    "q17": {"b": "q21", "c": "&1"},
    "q18": {"a": "q10", "c": "q22"},
    "q19": {"b": "q21"},
    "q20": {"c": "q7"},
    "q21": {"c": "q12"},
    "q22": {"a": "q23", "b": "q15"},
    "q23": {"a": "q19", "b": "q20", "c": "&1"},
}

AFA_FINAL = {
    "q1", "q2", "q3", "q4", "q5", "q6", "q8",
    "q16", "q17", "q19", "q24", "q25", "q27", "q30"
}

REGEX = r'((aa|bb)*)(b*|(a|a((bc|ac)*b)a|(abc|bca)*)a)|ab'

dfa = DFA(DFA_TRANSITIONS, DFA_START, DFA_FINAL)
nfa = NFA(NFA_TRANSITIONS, NFA_START, NFA_FINAL)
afa = AFA(AFA_TRANSITIONS, AFA_FINAL)

alphabet = ["a", "b", "c"]
words = generate_words(alphabet, 1, 20, 3000)

# Фазз-тестирование эквивалентности регулярного выражения, НКА, минимального ДКА и ПКА
for w in words:
    r = check_regex(w)
    n = nfa.accepts(w)
    d = dfa.accepts(w)
    p = afa.accepts(w)

    if not (r == n == d == p):
        print("Несовпадение")
        print("слово:", w)
        print("рег.:", r, "НКА:", n, "ДКА:", d, "ПКА:", p)
        break
else:
    print("Все автоматы эквивалентны друг другу и регулярному выражению на сгенерированном батче")

