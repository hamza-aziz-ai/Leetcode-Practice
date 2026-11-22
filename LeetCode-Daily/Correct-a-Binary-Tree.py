# LeetCode 1660. Correct a Binary Tree (Medium)
#
# One node's right pointer was bent sideways: it points to another node on the
# same level, somewhere to its right. Remove that bad node and everything under
# it (but not the node it wrongly points to), and return the root.
#
# Level by level, right to left: on each level, visit the nodes from right to
#     left. The bad node's right pointer leads to a node already seen on this
#     level; no good node's can. Cut the bad node from its parent. O(n).
# Right-first DFS: the same idea with one visited set: visit right subtrees
#     before left ones, so the wrongly pointed-to node is always seen first.
#     O(n), but recursion as deep as the tree.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def correctBinaryTree(self, root: TreeNode) -> TreeNode:
        level = [(root, None)]
        while level:
            seen = set()
            nxt = []
            for node, par in level:
                if node.right in seen:
                    if par.left is node:
                        par.left = None
                    else:
                        par.right = None
                    return root
                seen.add(node)
                if node.right:
                    nxt.append((node.right, node))
                if node.left:
                    nxt.append((node.left, node))
            level = nxt
        return root


class SolutionDFS:
    def correctBinaryTree(self, root: TreeNode) -> TreeNode:
        seen = set()

        def fix(node):
            if node is None:
                return None
            if node.right in seen:
                return None
            seen.add(node)
            node.right = fix(node.right)
            node.left = fix(node.left)
            return node

        return fix(root)


def mistakes():
    def left_to_right(root):
        # walks each level left to right: the bad node is met before the node it points to
        level = [(root, None)]
        while level:
            seen = set(); nxt = []
            for node, par in level:
                if node.right in seen:
                    if par.left is node: par.left = None
                    else: par.right = None
                    return root
                seen.add(node)
                if node.left: nxt.append((node.left, node))
                if node.right: nxt.append((node.right, node))
            level = nxt
        return root

    def cut_pointer_only(root):
        # clears the bad right pointer but keeps the bad node and its left subtree
        level = [(root, None)]
        while level:
            seen = set(); nxt = []
            for node, par in level:
                if node.right in seen:
                    node.right = None
                    return root
                seen.add(node)
                if node.right: nxt.append((node.right, node))
                if node.left: nxt.append((node.left, node))
            level = nxt
        return root

    def left_first_dfs(root):
        # visits left subtrees first, so the bad node is reached before its target
        seen = set()
        def fix(node):
            if node is None: return None
            if node.right in seen: return None
            seen.add(node)
            node.left = fix(node.left)
            node.right = fix(node.right)
            return node
        return fix(root)

    return left_to_right, cut_pointer_only, left_first_dfs


# ---------- helpers for testing ----------
def build(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0]); q = [root]; i = 1; k = 0
    while i < len(vals):
        node = q[k]; k += 1
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root


def find(root, v):
    st = [root]; seen = set()
    while st:
        x = st.pop()
        if x is None or id(x) in seen:
            continue
        seen.add(id(x))
        if x.val == v:
            return x
        st += [x.left, x.right]


def dump(root):
    out, q, k = [], [root], 0
    while k < len(q):
        x = q[k]; k += 1
        out.append(None if x is None else x.val)
        if x is not None:
            q += [x.left, x.right]
    while out and out[-1] is None:
        out.pop()
    return out


def expected(vals, frm):
    # the tree without the bad node and its subtree, built straight from the clean input
    root = build(vals)
    st = [root]
    while st:
        x = st.pop()
        for side in ("left", "right"):
            c = getattr(x, side)
            if c is not None:
                if c.val == frm:
                    setattr(x, side, None)
                else:
                    st.append(c)
    return dump(root)


def defective(vals, frm, to):
    root = build(vals)
    find(root, frm).right = find(root, to)
    return root


def random_case(n):
    # a random tree, then a bad node with no right child and a target to its right on the same level
    while True:
        vals = list(range(1, n + 1)); root = TreeNode(vals[0]); nodes = [root]
        for v in vals[1:]:
            while True:
                p = nodes[__import__("random").randrange(len(nodes))]
                side = __import__("random").choice(("left", "right"))
                if getattr(p, side) is None:
                    setattr(p, side, TreeNode(v)); nodes.append(getattr(p, side)); break
        lv = dump(root)
        levels = []; level = [root]
        while level:
            levels.append(level); level = [c for x in level for c in (x.left, x.right) if c]
        pairs = [(a.val, b.val) for L in levels for i, a in enumerate(L) for b in L[i + 1:] if a.right is None]
        if pairs:
            frm, to = __import__("random").choice(pairs)
            return lv, frm, to


if __name__ == "__main__":
    import random
    import time

    for vals, frm, to, want in (([1, 2, 3], 2, 3, [1, None, 3]), ([8, 3, 1, 7, None, 9, 4, 2, None, None, None, 5, 6], 7, 4, [8, 3, 1, None, None, 9, 4, None, None, 5, 6])):
        for s in (Solution(), SolutionDFS()):
            assert dump(s.correctBinaryTree(defective(vals, frm, to))) == want, (type(s).__name__, vals)
    for _ in range(5000):
        vals, frm, to = random_case(random.randint(3, 12))
        want = expected(vals, frm)
        for s in (Solution(), SolutionDFS()):
            got = dump(s.correctBinaryTree(defective(vals, frm, to)))
            assert got == want, (type(s).__name__, vals, frm, to, got, want)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            vals, frm, to = random_case(random.randint(3, 6))
            try:
                got = dump(f(defective(vals, frm, to)))
            except RecursionError:
                got = "error"
            if got != expected(vals, frm):
                if found is None or len(vals) < len(found[0]):
                    found = (vals, frm, to, got)
        print(f.__name__, "fails on root, fromNode, toNode =", found[:3], "->", found[3], "instead of", expected(found[0], found[1])) if found else print(f.__name__, "found no failure")

    # a full tree of 2^14 - 1 nodes, bad pointer on the bottom level
    vals = list(range(1, 2 ** 14))
    root = defective(vals, 2 ** 13, 2 ** 14 - 1)
    for s in (Solution(), SolutionDFS()):
        root = defective(vals, 2 ** 13, 2 ** 14 - 1)
        t0 = time.time(); s.correctBinaryTree(root); print("full tree, 16383 nodes:", type(s).__name__, f"{time.time() - t0:.3f}s")
    # a long left spine: recursion depth 5000
    n = 5000
    spine = [1]
    for v in range(2, n + 1):
        spine += [v, None]
    spine = spine[:-1]
    root = build(spine)
    leaf = root
    while leaf.left:
        leaf = leaf.left
    deep_ok = True
    try:
        SolutionDFS().correctBinaryTree(root)
    except RecursionError:
        deep_ok = False
    print("left spine of 5000 nodes, SolutionDFS without raising the recursion limit:", "ok" if deep_ok else "RecursionError")
    t0 = time.time(); Solution().correctBinaryTree(build(spine)); print("left spine of 5000 nodes: Solution", f"{time.time() - t0:.3f}s")
