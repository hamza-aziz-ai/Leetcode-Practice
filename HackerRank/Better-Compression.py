# HackerRank: Better Compression ("Question 1")
#
# S is a list of groups, each a lowercase letter followed by a whole number,
# like "a3c9b2c1". The same letter may appear more than once. Return each letter
# once, in alphabetical order, with the sum of all its numbers: "a3b2c10".
#
# Read S left to right. A letter starts a group; the digits after it make the
# number, which can have several digits (10, 1000), so build it digit by digit:
# num = num * 10 + digit. Add it to that letter's total in a 26-slot list, then
# write out the letters with a non-zero total, a to z. O(len(S)).
import re


def betterCompression(s):
    counts = [0] * 26
    i = 0
    while i < len(s):
        ch = s[i]
        i += 1
        num = 0
        while i < len(s) and s[i].isdigit():
            num = num * 10 + int(s[i])
            i += 1
        counts[ord(ch) - ord('a')] += num
    out = []
    for k in range(26):
        if counts[k] > 0:
            out.append(chr(ord('a') + k) + str(counts[k]))
    return "".join(out)


def betterCompressionRegex(s):
    # the same, letting a regular expression split the groups
    totals = {}
    for ch, num in re.findall(r"([a-z])(\d+)", s):
        totals[ch] = totals.get(ch, 0) + int(num)
    return "".join(ch + str(totals[ch]) for ch in sorted(totals))


def mistakes():
    def one_digit(s):
        # reads only one digit after each letter
        counts = [0] * 26
        for i in range(0, len(s) - 1):
            if s[i].isalpha():
                counts[ord(s[i]) - 97] += int(s[i + 1])
        return "".join(chr(97 + k) + str(c) for k, c in enumerate(counts) if c)

    def keep_first_order(s):
        # merges the counts but keeps the order letters first appear in
        totals = {}
        for ch, num in re.findall(r"([a-z])(\d+)", s):
            totals[ch] = totals.get(ch, 0) + int(num)
        return "".join(ch + str(n) for ch, n in totals.items())

    return one_digit, keep_first_order


if __name__ == "__main__":
    import random
    import time

    assert betterCompression("a3c9b2c1") == "a3b2c10"
    assert betterCompressionRegex("a3c9b2c1") == "a3b2c10"

    def make(groups):
        return "".join(f"{c}{n}" for c, n in groups)

    def expect(groups):
        tot = {}
        for c, n in groups:
            tot[c] = tot.get(c, 0) + n
        return "".join(f"{c}{tot[c]}" for c in sorted(tot))

    for _ in range(5000):
        groups = [(random.choice("abcdefghijklmnopqrstuvwxyz"[: random.randint(1, 26)]), random.choice([1, 9, 10, 99, 100, 1000, random.randint(1, 1000)])) for _ in range(random.randint(1, 12))]
        s = make(groups)
        assert betterCompression(s) == expect(groups) == betterCompressionRegex(s), s
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            groups = [(random.choice("abc"), random.randint(1, 12)) for _ in range(random.randint(1, 3))]
            s = make(groups)
            if f(s) != expect(groups) and (found is None or len(s) < len(found)):
                found = s
        print(f.__name__, "fails on", repr(found), "->", repr(f(found)), "instead of", repr(betterCompression(found))) if found else print(f.__name__, "found no failure")

    groups = [(random.choice("abcdefghijklmnopqrstuvwxyz"), random.randint(1, 1000)) for _ in range(25000)]
    s = make(groups)[:100000]
    s = s.rstrip("abcdefghijklmnopqrstuvwxyz")
    for f in (betterCompression, betterCompressionRegex):
        t0 = time.time(); f(s); print(f"len(S) = {len(s)}:", f.__name__, f"{time.time() - t0:.3f}s")
