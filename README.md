# DeepThought CultureTech Ventures — DT Fellowship Assignment
### The Daily Reflection Tree

---

## Overview

This repository contains my submission for the DT Fellowship Assignment — a deterministic end-of-day reflection tool built as a structured decision tree, with an optional AI Agent that walks the tree programmatically.

The tool guides an employee through a structured evening reflection across **three psychological axes**. Every question has fixed options. Every option leads to a known branch. No LLM is called at runtime — the same answers always produce the same reflection, every time.

> **The tree is the product. The LLM was the power tool used to build it.**

---

## Repository Structure

```
/submission/
  /tree/
    reflection-tree.json     ← Part A: Full decision tree (30 nodes, all 3 axes)
    tree-diagram.md          ← Part A: Mermaid flowchart of all branches
  /agent/                    ← Part B (Bonus): Runnable CLI agent
    ...
  /transcripts/              ← Part B (Bonus): Sample runs
    persona-1-transcript.md  ← "Victim / Entitled / Self-centric" persona
    persona-2-transcript.md  ← "Victor / Contributing / Altrocentric" persona
  write-up.md                ← Part A: Design rationale (2 pages)
README.md
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
| `signal` | What gets tallied in state (e.g. `locus:internal` adds 1 to the internal locus counter) |
| `next` | Where to go after this node (non-question nodes) |
| `condition` | Routing logic for decision nodes — checks which signal is dominant |

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

## Part B — The AI Agent (Bonus)

### What It Does

A CLI program that:
- **Loads** the tree from `reflection-tree.json` (not hardcoded)
- **Walks** the tree — renders each node, waits for input at question nodes, auto-advances at non-interactive nodes
- **Branches deterministically** — selected option → next node, no randomness, no LLM calls
- **Accumulates state** — tracks selections and tallies per-axis signals
- **Interpolates** reflection text with the employee's earlier answers
- **Produces a reflection summary** combining all three axis outcomes

### How to Run

```bash
cd submission/agent
pip install -r requirements.txt
python agent.py
```

### Sample Transcripts

Two full sample runs are included in `/submission/transcripts/`:

- **Persona 1** (`persona-1-transcript.md`) — External locus, entitlement orientation, self-focused radius
- **Persona 2** (`persona-2-transcript.md`) — Internal locus, giving orientation, transcendent radius

Both transcripts show how the tree branched differently and produced different reflections for each persona.

---

## Key Design Decisions

- **Accumulated signals, not single gates** — One "off" answer doesn't derail the path. The dominant signal across all questions in an axis determines the branch, making the tool forgiving of mixed days.
- **Tied cases handled explicitly** — Each axis has a dedicated `REFLECT_MIXED` node — not a fallback, but a genuinely written response for the most common real outcome.
- **No moralizing** — The "victim" and "entitlement" paths don't shame the employee. They invite reflection with the tone of a wise colleague.
- **4 options per question** — 3 feels too binary; 5 creates paralysis at 7pm. 4 is the sweet spot.
- **Depth over breadth** — 2 questions per axis with real branching beats 5 surface questions with no branches.

---

## Psychological Sources

| Framework | Author | Year |
|-----------|--------|------|
| Locus of Control | Julian Rotter | 1954 |
| Growth Mindset | Carol Dweck | 2006 |
| Psychological Entitlement | Campbell et al. | 2004 |
| Organizational Citizenship Behavior | Dennis Organ | 1988 |
| Self-Transcendence | Abraham Maslow | 1969 |
| Perspective-Taking | Daniel Batson | 2011 |

---

## Assignment Brief

Original assignment: [DailyReflectionTree.md](https://github.com/DT-CultureTech/recruitmentassignments/blob/main/DailyReflectionTree.md)

Submitted by: **Kumar Shailesh**  
Deadline: April 24, 2026
