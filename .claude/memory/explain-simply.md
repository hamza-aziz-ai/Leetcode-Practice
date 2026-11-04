---
name: explain-simply
description: "Explain LeetCode problems in very simple language, as if to a 5 year old, moving from idea to algorithm to code, starting from brute force when needed, and showing how variables change at each step"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 831ffb31-a75b-4ecf-a158-a44aedc75dc6
  modified: 2026-11-01T09:15:56.753Z
---

Keep every explanation as simple as possible, as if explaining to a 5 year old child. Use very simple language and do not go technical right away. Lead the user from idea to algorithm, then from algorithm to code. If the optimal solution is hard to grasp at first look, start with brute force and then move step by step to the optimal solution. Show how the value of each variable changes at each step.

**Why:** The user asked for this to always be remembered after reviewing the LeetCode explainer artifacts. The aim is real understanding of the solution, not a compact proof.

**How to apply:** Use plain words, everyday pictures, and small concrete examples, and introduce a term only when it is needed. Keep code, formulas, and notation out of the opening; give the idea first, then plain numbered steps, then the code that matches those steps. In artifacts and walkthroughs, when the optimal idea needs a leap, show the slow approach first, show why it is slow, then let each step lead to the faster one. If the optimal idea is obvious at first look, skip brute force. Every animated code stage gets a variable table with one row per step, the current row marked, and the changed values highlighted. Variable names in that table must match the code on the page exactly, and the code should be written so its variables are visible, which may mean a small loop instead of a one-liner. Page layout rules are in [[artifact-text-layout]].

**Debugger walkthroughs (added 2026-11-04):** For hard problems, the user lost track of the optimal solution when the page only animated pictures. They asked to be taught like a beginner who wants every detail. So every code stage is a debugger, not just a player. It has Step in, Step over, Step out and Back. It shows the current line, a Variables panel with changed values marked, and an Evaluating panel that works each expression out piece by piece (for example `range(n - x + 1)` → `range(7 - 3 + 1)` → `range(5)` → `0..4`). A debug log keeps one row per stop. Step in must open up every hidden loop or Python idiom (`combinations`, `zip(a, a[1:])`, `any(...)`, `sum(... for ...)`, list comprehensions, `range` bounds), say why each bound has its `+ 1` or starts where it does, and say how each loop ends. Add a "Python tools you will meet" table with real values. When going from brute force to optimal, show the path as small stops, each removing one waste, and say which clues in the problem hint at each idea.

**Concept to code journey (added 2026-11-04):** The user wants as much animation as possible. For every stage, show three things in order. First, a concept animation that plays by itself when scrolled into view and has Play, Back and Step controls (things moving, such as cards flying, frames jumping, or arrows racing). Second, a "journey" panel with three columns: plain steps, pseudo-code and Python. As each plain step lights up, its pseudo-code lines highlight and its Python lines are typed in. A table under the columns shows which words turned into which code. Third, the line-by-line debugger.
