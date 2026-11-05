# LeetCode 1032. Stream of Characters (Hard)
#
# Letters arrive one at a time. After each letter, answer: does the stream
# so far END with one of the words?
#
# Slow way: after each letter, check every word with endswith.
#           query: O(total length of all words), up to 400,000 letter checks.
# Reversed trie: put every word into a trie BACKWARDS. After each letter,
#           read the stream backwards from the newest letter and walk the
#           trie. Stop when the path breaks (False) or a word ends (True).
#           query: O(L), L = longest word (at most 200), usually much less.
# Aho-Corasick: a forward trie plus "fall back" links. One pointer moves
#           one step per letter, so query is O(1) on average.
from collections import deque
from typing import List


class StreamCheckerSlow:
    def __init__(self, words: List[str]):
        self.words = words
        self.stream = ""

    def query(self, letter: str) -> bool:
        self.stream += letter
        for w in self.words:
            if self.stream.endswith(w):
                return True
        return False


class StreamChecker:
    def __init__(self, words: List[str]):
        self.root = {}
        for w in words:
            node = self.root
            for ch in reversed(w):
                node = node.setdefault(ch, {})
            node["$"] = True
        self.stream = []
        self.longest = max(len(w) for w in words)

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        node = self.root
        for ch in reversed(self.stream[-self.longest:]):
            if ch not in node:
                return False
            node = node[ch]
            if "$" in node:
                return True
        return False


class StreamCheckerAhoCorasick:
    def __init__(self, words: List[str]):
        self.children = [{}]          # node 0 is the root
        self.fail = [0]               # where to fall back when the next letter has no branch
        self.out = [False]            # does some word end at this node, or at a node it falls back to?
        for w in words:
            node = 0
            for ch in w:
                if ch not in self.children[node]:
                    self.children.append({})
                    self.fail.append(0)
                    self.out.append(False)
                    self.children[node][ch] = len(self.children) - 1
                node = self.children[node][ch]
            self.out[node] = True
        queue = deque(self.children[0].values())
        while queue:                  # breadth first, so shorter nodes are finished first
            u = queue.popleft()
            for ch, v in self.children[u].items():
                f = self.fail[u]
                while f and ch not in self.children[f]:
                    f = self.fail[f]
                self.fail[v] = self.children[f].get(ch, 0)
                self.out[v] = self.out[v] or self.out[self.fail[v]]
                queue.append(v)
        self.node = 0

    def query(self, letter: str) -> bool:
        node = self.node
        while node and letter not in self.children[node]:
            node = self.fail[node]
        self.node = self.children[node].get(letter, 0)
        return self.out[self.node]


if __name__ == "__main__":
    import random
    import time

    def run(cls, words, letters):
        sc = cls(words)
        return [sc.query(c) for c in letters]

    want = [False, False, False, True, False, True, False, False, False, False, False, True]
    for cls in (StreamCheckerSlow, StreamChecker, StreamCheckerAhoCorasick):
        assert run(cls, ["cd", "f", "kl"], "abcdefghijkl") == want
    for _ in range(4000):
        alpha = "abc"[: random.randint(1, 3)]
        words = ["".join(random.choice(alpha) for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 6))]
        letters = "".join(random.choice(alpha) for _ in range(random.randint(1, 25)))
        a = run(StreamCheckerSlow, words, letters)
        assert run(StreamChecker, words, letters) == a, (words, letters)
        assert run(StreamCheckerAhoCorasick, words, letters) == a, (words, letters)
    print("all tests pass")

    # Worst-ish case for the reversed trie: long words that almost match.
    words = ["a" * 199 + "b"] + ["".join(random.choice("ab") for _ in range(200)) for _ in range(1999)]
    letters = "a" * 40000
    for cls in (StreamChecker, StreamCheckerAhoCorasick):
        t = time.time(); run(cls, words, letters); print(cls.__name__, f"{time.time() - t:.2f}s")
