---
name: artifact-text-layout
description: "Text layout rules for artifacts and written output: no forced line breaks, justified paragraphs, full-width paragraphs with no max-width"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 831ffb31-a75b-4ecf-a158-a44aedc75dc6
  modified: 2026-11-01T08:51:44.437Z
---

Never use line breaks to force-wrap text. In artifacts, paragraphs are justified (`text-align: justify; hyphens: auto`) and span the full width of their container, so never cap them with a `max-width` such as `68ch`. This overrides the artifact-design guidance to keep running text near 65 characters wide.

**Why:** The user corrected this after two LeetCode explainer artifacts capped paragraphs at `68ch`, leaving them narrower than the page. The user asked for this to always be remembered.

**How to apply:** For every artifact, set paragraphs and list items to `width: 100%` with justified text, and let the renderer wrap. Check the CSS for `max-width` on `p`, `li`, and prose containers before publishing.
