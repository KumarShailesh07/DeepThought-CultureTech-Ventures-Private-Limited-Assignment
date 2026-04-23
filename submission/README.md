# The Daily Reflection Tree
### DT Fellowship Assignment — Part A Submission

---

## What This Is

An end-of-day deterministic reflection tool. An employee answers fixed-choice questions across three psychological axes. The tree branches based on their answers and produces a personalised reflection — with no AI, no free text, no ambiguity.

**Same answers → same path → same reflection. Every time.**

---

## Files

```
/tree/
  reflection-tree.json   ← The full tree (30 nodes, all 3 axes)
  tree-diagram.md        ← Mermaid flowchart of all branches
  write-up.md            ← Design rationale (2 pages)
README.md
```

---

## How to Read the Tree

Open `reflection-tree.json`. Each node has:

| Field | What it means |
|-------|--------------|
| `id` | Unique identifier for this node |
| `type` | What kind of node: `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees |
| `options` | Fixed choices (questions only). Each option has a `next` node and optional `signal` |
| `signal` | What gets tallied in state: e.g. `locus:internal` adds 1 to the internal locus counter |
| `next` | Where to go after this node (non-question nodes) |
| `condition` | Routing logic for decision nodes — checks which signal is dominant |

### Node Types

| Type | Employee sees it? | What it does |
|------|------------------|--------------|
| `start` | Yes — auto-advances | Opens the session |
| `question` | Yes — waits for click | Asks a question with fixed options |
| `decision` | No — invisible | Routes based on accumulated signals |
| `reflection` | Yes — click to continue | Shows a reframe based on the path taken |
| `bridge` | Yes — auto-advances | Transitions between axes |
| `summary` | Yes — click to continue | End-of-session synthesis |
| `end` | Yes — auto-advances | Closes the session |

---

## How to Trace a Path

Example: Employee says today was "Draining", then "What went wrong", then "I had no say":

```
START → Q_OPEN (picks "Draining") 
      → A1_Q1_LOW (picks "What went wrong") [signal: locus:external]
      → A1_Q2 (picks "I had no say") [signal: locus:external]
      → A1_DECISION (external dominant, 2-0)
      → A1_REFLECT_EXTERNAL
      → BRIDGE_1_2
      → A2_Q1 ...
```

Every path is fully traceable without running any code.

---

## Three Axes

| Axis | Spectrum | Psychology |
|------|----------|-----------|
| 1 — Locus | Victim ↔ Victor | Rotter (1954), Dweck (2006) |
| 2 — Contribution | Entitlement ↔ Giving | Campbell et al. (2004), Organ (1988) |
| 3 — Radius | Self ↔ Transcendent | Maslow (1969), Batson (2011) |

---

## Node Count

| Type | Count |
|------|-------|
| start / end | 2 |
| question | 7 |
| decision | 3 |
| reflection | 10 |
| bridge | 2 |
| summary | 1 |
| **Total** | **30** |
