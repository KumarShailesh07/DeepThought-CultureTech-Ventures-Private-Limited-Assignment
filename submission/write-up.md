# Write-Up: The Daily Reflection Tree
## Design Rationale

---

### Why These Questions

The hardest constraint in designing this tree was the **no free text rule** — every question must have fixed options, yet those options must feel like they were written for *me specifically*, not pulled from a survey. That forced a discipline: every option had to do real psychological work, not just cover a category.

**On Axis 1 (Locus of Control)**, the opening question branches on overall mood — not because mood is the outcome we're measuring, but because it changes *which version of the locus question is fair to ask*. Someone who had a draining day and is asked "what made things go well?" will disengage immediately. The tree respects the employee's actual emotional state before probing their relationship with agency. This is rooted in Rotter's (1954) insight that locus is revealed not in success stories but in how people narrate *setbacks* — so the low-energy path asks directly about hard moments.

Dweck's (2006) growth mindset work informed the second question on this axis: "Was there a moment you made a call — even a small one?" The word *even* is deliberate. It lowers the bar enough that someone who felt powerless all day can still honestly say yes — while also surfacing whether they were *looking for* those moments at all.

**On Axis 2 (Contribution vs Entitlement)**, Campbell et al. (2004) note that entitlement is invisible to the person holding it. Entitled people don't feel greedy — they feel *owed*. So the questions avoid any framing that signals "entitlement is bad." Both options in each pair are presented with equal dignity. "I felt my effort went unnoticed" is not shamed — it's named. The reflection node for the entitlement path doesn't moralize; it poses a genuine question: *what would it feel like to give without keeping score?* That's an invitation, not a verdict.

**On Axis 3 (Radius of Concern)**, Maslow's 1969 paper on self-transcendence — the tier above self-actualization he added late in his career — frames the goal not as selflessness but as *perspective expansion*. The questions use concentric circles: just me → one other → the team → downstream stakeholders. This gives the employee a navigation tool, not a judgment. Batson's (2011) perspective-taking research informed the second question: "Did anyone today have it harder than you — and did you notice?" The *and did you notice* is the key phrase. It separates awareness from action — two different things worth distinguishing.

---

### How the Branching Works

The tree uses **accumulated signals**, not a single gate. Every question node tags its answer with a signal (`locus:internal`, `locus:external`, etc.). Decision nodes look at the *dominant* signal at the end of each axis — whichever pole has more tallies wins.

This means a single "off" answer doesn't derail the path. Someone who mostly demonstrated internal locus but admitted they felt stuck once doesn't get routed to the "victim" branch. The system is forgiving by design — because real days are mixed, and a tool that dramatically reroutes on one answer will feel punitive.

The **tied case** gets its own reflection node (e.g., `A1_REFLECT_MIXED`) — not a fallback, but a genuinely written response for the most common real outcome: most people have days that are split.

**Trade-offs made:**
- I chose depth over breadth — 2 questions per axis with real branching beats 5 surface questions with no branches.
- I kept the options at 4 per question. 3 feels too binary; 5 creates paralysis at 7pm when someone just wants to reflect and sleep.
- The summary node uses **combinatorial pre-written reflections** keyed to axis combinations (e.g., `internal+giving+self`). With 3 axes and 2-3 poles each, there are 8 primary combinations — all written out explicitly. No generation needed.

---

### Psychological Sources

| Framework | Author | Year | Where it appears |
|-----------|--------|------|-----------------|
| Locus of Control | Julian Rotter | 1954 | Axis 1 question design and branching |
| Growth Mindset | Carol Dweck | 2006 | Axis 1, Q2 — "even a small call" |
| Psychological Entitlement | Campbell et al. | 2004 | Axis 2 option design and reflections |
| Organizational Citizenship Behavior | Dennis Organ | 1988 | Axis 2 — defining "giving" behaviours |
| Self-Transcendence | Abraham Maslow | 1969 | Axis 3 — concentric radius structure |
| Perspective-Taking | Daniel Batson | 2011 | Axis 3, Q2 — noticing vs acting |

---

### What I'd Improve With More Time

1. **Streaks and deltas.** The tree currently treats every session independently. With persistent state across sessions, the summary could say: *"This is the third evening in a row you leaned external. Worth a look."* That's where the tool gets genuinely powerful — when it reflects patterns, not just today.

2. **More branches within axes.** Right now each axis has one decision node at the end. A richer design would branch *within* the axis — so a strongly external respondent gets a different Q2 than a mildly external one. More nodes, but more precise.

3. **A "challenge mode."** For employees who've been using the tool for 30+ days and consistently land in the same quadrant, the tree could offer a harder version of each question — one that probes the comfortable narrative rather than confirming it.

4. **Session timing awareness.** A reflection started at 6pm should feel different from one started at 11pm. The opening node could branch on session time to adjust tone — warmer and more direct when the employee is tired.

---

*Total nodes: 30 | Question nodes: 7 | Decision nodes: 3 | Reflection nodes: 10 | Bridge nodes: 2 | Summary: 1 | Start/End: 2*
