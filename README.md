# DeepThought CultureTech Ventures — DT Fellowship Assignment
### The Daily Reflection Tree

---

## Overview

This repository contains my submission for the DT Fellowship Assignment — a deterministic end-of-day reflection tool built as a structured decision tree, with a working CLI agent that walks the tree programmatically.

The tool guides an employee through a structured evening reflection across **three psychological axes**. Every question has fixed options. Every option leads to a known branch. No LLM is called at runtime — the same answers always produce the same reflection, every time.

> **The tree is the product. The LLM was the power tool used to build it.**

---

## Repository Structure

```
/submission/
  /tree/
    reflection-tree.json       ← Part A: Full decision tree (30 nodes, all 3 axes)
    tree-diagram.md            ← Part A: Mermaid flowchart of all branches
    tree-diagram.png           ← Part A: Visual diagram
  /agent/
    agent.py                   ← Part B: Runnable CLI agent (pure Python, no dependencies)
  /transcripts/
    persona-1-transcript.md    ← Part B: "Victim / Entitled / Self-centric" persona
    persona-2-transcript.md    ← Part B: "Victor / Contributing / Altrocentric" persona
  write-up.md                  ← Part A: Design rationale (2 pages)
  README.md                    ← Submission-level README
README.md                      ← This file
```

---

## Part A — The Decision Tree

### What It Is

An end-of-day deterministic reflection tool. An employee answers fixed-choice questions across three psychological axes. The tree branches based on their answers and produces a personalised reflection — with no AI, no free text, no ambiguity.

**Same answers → same path → same reflection. Every time.**

### The Three Axes

| Axis | Spectrum | Psychological Basis |
|------|----------|-------------------|
| 1 — Locus | Victim ↔ Victor | Rotter (1954), Dweck (2006) |
| 2 — Contribution | Entitlement ↔ Giving | Campbell et al. (2004), Organ (1988) |
| 3 — Radius | Self ↔ Transcendent | Maslow (1969), Batson (2011) |

### Node Count

| Type | Count |
|------|-------|
| start / end | 2 |
| question | 7 |
| decision | 3 |
| reflection | 10 |
| bridge | 2 |
| summary | 1 |
| **Total** | **30** |

### How to Read the Tree

Open `submission/tree/reflection-tree.json`. Each node has:

| Field | What it means |
|-------|--------------|
| `id` | Unique identifier for this node |
| `type` | Node type: `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees |
| `options` | Fixed choices (question nodes only). Each option has a `next` node and optional `signal` |
| `signal` | What gets tallied in state — e.g. `locus:internal` adds 1 to the internal locus counter |
| `next` | Where to go after this node (non-question nodes) |
| `axis` | Which axis this node belongs to (used by decision nodes to check dominant signal) |
| `routes` | Routing table for decision nodes — maps dominant pole → next node id |

### How to Trace a Path (Example)

Employee says today was **"Draining"**, then **"What went wrong"**, then **"I had no say"**:

```
START → Q_OPEN (picks "Draining")
      → A1_Q1_LOW (picks "What went wrong") [signal: locus:external]
      → A1_Q2 (picks "I had no say")        [signal: locus:external]
      → A1_DECISION (external dominant, 2-0)
      → A1_REFLECT_EXTERNAL
      → BRIDGE_1_2
      → A2_Q1 ...
```

Every path is fully traceable without running any code.

---

## Part B — The CLI Agent

### Requirements

- **Python 3.7+**
- **No external libraries** — uses only the Python standard library (`json`, `os`, `sys`, `time`, `collections`)

### How to Run

```bash
cd submission/agent
python agent.py
```

The agent automatically finds `reflection-tree.json` — it looks in the same folder as the script, then in `../tree/`. No configuration needed.

### What the Agent Does

- **Loads** the tree from `reflection-tree.json` (not hardcoded in source)
- **Walks** the tree — renders each node, waits for input at question nodes, auto-advances at non-interactive nodes
- **Branches deterministically** — selected option → next node, no randomness, no LLM calls
- **Accumulates state** — tracks selections and tallies per-axis signals using a dominant-signal algorithm
- **Produces a personalised summary** combining all three axis outcomes at the end

### How Branching Works

As the employee answers, each option records a **signal** (`axis:pole`). At the end of each axis, a decision node checks which pole is dominant and routes accordingly:

```
signal: locus:internal  →  state.signals["locus"]["internal"] += 1
signal: locus:external  →  state.signals["locus"]["external"] += 1

decision node checks: dominant("locus")
  → "internal"  : go to A1_REFLECT_INTERNAL
  → "external"  : go to A1_REFLECT_EXTERNAL
  → "tied"      : go to A1_REFLECT_MIXED
```

No scoring model. No LLM. Just tallies and lookups.

### Sample Transcripts

Two full sample runs are in `/submission/transcripts/`:

| File | Persona |
|------|---------|
| `persona-1-transcript.md` | External locus · Entitlement orientation · Self-focused radius |
| `persona-2-transcript.md` | Internal locus · Giving orientation · Transcendent radius |

Both show how the tree branched differently and produced different reflections.

---

## Design Highlights

- **Accumulated signals, not single gates** — one "off" answer doesn't derail the path. The dominant signal across all questions in an axis determines the branch, making the tool forgiving of mixed days.
- **Tied cases handled explicitly** — each axis has a dedicated `REFLECT_MIXED` node — a genuinely written response for the most common real outcome, not a fallback.
- **No moralizing** — the "victim" and "entitlement" paths don't shame the employee. They invite reflection with the tone of a wise colleague.
- **4 options per question** — 3 feels too binary; 5 creates paralysis at 7pm. 4 is the sweet spot.
- **8 pre-written summary reflections** — keyed to axis combinations (e.g. `internal+giving+transcendent`), covering all primary outcomes explicitly. No generation needed.

---

## Psychological Sources

| Framework | Author | Year | Where it appears |
|-----------|--------|------|-----------------|
| Locus of Control | Julian Rotter | 1954 | Axis 1 question design and branching |
| Growth Mindset | Carol Dweck | 2006 | Axis 1 Q2 — "even a small call" |
| Psychological Entitlement | Campbell et al. | 2004 | Axis 2 option design and reflections |
| Organizational Citizenship Behavior | Dennis Organ | 1988 | Axis 2 — defining "giving" behaviours |
| Self-Transcendence | Abraham Maslow | 1969 | Axis 3 — concentric radius structure |
| Perspective-Taking | Daniel Batson | 2011 | Axis 3 Q2 — noticing vs acting |

---

## Assignment Brief

Original assignment: [DailyReflectionTree.md](https://github.com/DT-CultureTech/recruitmentassignments/blob/main/DailyReflectionTree.md)

Submitted by: **Shailesh Kumar**  
