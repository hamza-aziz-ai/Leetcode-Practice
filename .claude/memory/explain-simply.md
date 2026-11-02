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
