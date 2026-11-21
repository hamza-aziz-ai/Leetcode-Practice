# LeetCode 3331. Find Subtree Sizes After Changes (Medium)
#
# A tree rooted at 0 is given by parent[], and node i has letter s[i]. At the
# same time, every node x moves under its closest ancestor with the same letter
# (if there is one). Return the size of every subtree in the new tree.
#
# Climb and climb:      climb the old parents to find each new parent; then,
#                       for every node, climb the new parents adding 1 to each.
#                       O(n * depth).
# Sizes from the bottom: handle nodes deepest first and add each node's size to
#                       its new parent's. Finding the parents still climbs.
# Nearest of each letter: walk the tree top-down, carrying for each node the
#                       nearest node of every letter on its path (at most 26).
#                       The new parent is one lookup. O(26 n).
from typing import List


class SolutionClimb:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        newp = parent[:]
        for x in range(1, n):
            y = parent[x]
            while y != -1 and s[y] != s[x]:
                y = parent[y]
            if y != -1:
                newp[x] = y
        ans = [0] * n
        for x in range(n):
            y = x
            while y != -1:
                ans[y] += 1
                y = newp[y]
        return ans


class SolutionBottomUp:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        kids = [[] for _ in range(n)]
        for x in range(1, n):
            kids[parent[x]].append(x)
        order = [0]
        for x in order:
            order.extend(kids[x])
        newp = parent[:]
        for x in range(1, n):
            y = parent[x]
            while y != -1 and s[y] != s[x]:
                y = parent[y]
            if y != -1:
                newp[x] = y
        ans = [1] * n
        for x in reversed(order[1:]):
            ans[newp[x]] += ans[x]
        return ans


class Solution:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        kids = [[] for _ in range(n)]
        for x in range(1, n):
            kids[parent[x]].append(x)
        order = [0]
        for x in order:
            order.extend(kids[x])
        near = [None] * n
        near[0] = {s[0]: 0}
        newp = parent[:]
        for x in order[1:]:
            p = parent[x]
            if s[x] in near[p]:
                newp[x] = near[p][s[x]]
            near[x] = dict(near[p])
            near[x][s[x]] = x
        ans = [1] * n
        for x in reversed(order[1:]):
            ans[newp[x]] += ans[x]
        return ans


def mistakes():
    def one_at_a_time(parent, s):
        # applies the moves one node at a time, so later moves see earlier ones
        n = len(parent); par = parent[:]
        for x in range(1, n):
            y = par[x]
            while y != -1 and s[y] != s[x]:
                y = par[y]
            if y != -1:
                par[x] = y
        ans = [0] * n
        for x in range(n):
            y = x
            while y != -1:
                ans[y] += 1; y = par[y]
        return ans

    def index_order(parent, s):
        # adds sizes in index order n-1 .. 1 instead of deepest first
        n = len(parent); newp = parent[:]
        for x in range(1, n):
            y = parent[x]
            while y != -1 and s[y] != s[x]:
                y = parent[y]
            if y != -1:
                newp[x] = y
        ans = [1] * n
        for x in range(n - 1, 0, -1):
            ans[newp[x]] += ans[x]
        return ans

    def shared_near(parent, s):
        # changes the parent's dict instead of copying it, so siblings see each other
        n = len(parent); kids = [[] for _ in range(n)]
        for x in range(1, n):
            kids[parent[x]].append(x)
        order = [0]
        for x in order:
            order.extend(kids[x])
        near = [None] * n; near[0] = {s[0]: 0}; newp = parent[:]
        for x in order[1:]:
            p = parent[x]
            if s[x] in near[p]:
                newp[x] = near[p][s[x]]
            near[x] = near[p]
            near[x][s[x]] = x
        ans = [1] * n
        for x in reversed(order[1:]):
            ans[newp[x]] += ans[x]
        return ans

    return one_at_a_time, index_order, shared_near


if __name__ == "__main__":
    import random
    import time

    def random_tree(n, letters):
        parent = [-1] + [random.randint(0, i - 1) for i in range(1, n)]
        perm = list(range(1, n)); random.shuffle(perm); lab = [0] + perm
        inv = {lab[i]: i for i in range(n)}
        p2 = [-1] * n
        for i in range(1, n):
            p2[lab[i]] = lab[parent[i]]
        return p2, "".join(random.choice(letters) for _ in range(n))

    for parent, s, want in (([-1, 0, 0, 1, 1, 1], "abaabc", [6, 3, 1, 1, 1, 1]), ([-1, 0, 4, 0, 1], "abbba", [5, 2, 1, 1, 1])):
        for sol in (SolutionClimb(), SolutionBottomUp(), Solution()):
            assert sol.findSubtreeSizes(parent, s) == want, (type(sol).__name__, parent, s)
    for _ in range(5000):
        parent, s = random_tree(random.randint(1, 10), "abc")
        want = SolutionClimb().findSubtreeSizes(parent, s)
        for sol in (SolutionBottomUp(), Solution()):
            assert sol.findSubtreeSizes(parent, s) == want, (type(sol).__name__, parent, s)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            parent, s = random_tree(random.randint(1, 6), "ab")
            if f(parent, s) != Solution().findSubtreeSizes(parent, s):
                if found is None or len(parent) < len(found[0]):
                    found = (parent, s)
        print(f.__name__, "fails on", found, "->", f(*found), "instead of", Solution().findSubtreeSizes(*found)) if found else print(f.__name__, "found no failure")

    n = 4000
    chain = ([-1] + list(range(n - 1)), "a" * n)
    half = n // 2
    broom = ([-1] + list(range(half - 1)) + [half - 1] * half, "a" * half + "b" * half)
    for name, (parent, s) in (("chain of a", chain), ("a-chain with b leaves", broom)):
        for sol in (SolutionClimb(), SolutionBottomUp(), Solution()):
            t0 = time.time(); sol.findSubtreeSizes(parent, s); print(f"{name}, n = {n}:", type(sol).__name__, f"{time.time() - t0:.3f}s")
    N = 10**5
    parent = [-1] + [random.randint(max(0, i - 3), i - 1) for i in range(1, N)]
    s = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    t0 = time.time(); Solution().findSubtreeSizes(parent, s); print(f"deep random tree, n = {N}: Solution {time.time() - t0:.3f}s")
    parent = [-1] + list(range(N - 1)); s = "a" * N
    t0 = time.time(); Solution().findSubtreeSizes(parent, s); print(f"chain, n = {N}: Solution {time.time() - t0:.3f}s")
