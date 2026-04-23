#!/usr/bin/env python3
"""
The Daily Reflection Tree — CLI Agent
Loads reflection-tree.json and walks the employee through the conversation.
No LLM calls. Fully deterministic.
"""

import json
import os
import sys
import time
from collections import defaultdict


# ─── Colours (works on Mac/Linux/Windows Terminal) ────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
PURPLE = "\033[95m"
WHITE  = "\033[97m"
BLUE   = "\033[94m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text: str, delay: float = 0.018):
    """Print text character by character for a calm, deliberate feel."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def divider(char="─", width=55, color=DIM):
    print(color + char * width + RESET)


def print_header():
    clear()
    print()
    print(CYAN + BOLD + "  🌙  The Daily Reflection Tree" + RESET)
    divider()
    print()


# ─── Tree Loader ──────────────────────────────────────────────────────────────

def load_tree(path: str) -> dict:
    """Load the JSON tree and index nodes by id."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    index = {node["id"]: node for node in data["nodes"]}
    return index


# ─── State ────────────────────────────────────────────────────────────────────

class State:
    def __init__(self):
        # Signal tallies: { axis: { pole: count } }
        self.signals = defaultdict(lambda: defaultdict(int))
        # Every answer stored by node id
        self.answers = {}
        # Track which axis signals were collected
        self.axis_dominant = {}

    def record_signal(self, signal: str):
        """Parse 'axis:pole' and tally."""
        if not signal:
            return
        axis, pole = signal.split(":")
        self.signals[axis][pole] += 1

    def dominant(self, axis: str) -> str:
        """Return the dominant pole for an axis, or 'tied'."""
        poles = self.signals.get(axis, {})
        if not poles:
            return "tied"
        max_count = max(poles.values())
        leaders = [p for p, c in poles.items() if c == max_count]
        if len(leaders) == 1:
            return leaders[0]
        return "tied"

    def resolve_dominant(self, axis: str) -> str:
        """Get dominant and cache it."""
        d = self.dominant(axis)
        self.axis_dominant[axis] = d
        return d


# ─── Node Handlers ────────────────────────────────────────────────────────────

def handle_start(node: dict, state: State) -> str:
    print_header()
    print(WHITE + node["text"] + RESET)
    print()
    input(DIM + "  Press Enter to begin..." + RESET)
    return node["next"]


def handle_bridge(node: dict, state: State) -> str:
    print_header()
    print(DIM + "  ── " + RESET + YELLOW + node["text"] + RESET)
    print()
    time.sleep(0.5)
    input(DIM + "  Press Enter to continue..." + RESET)
    return node["next"]


def handle_reflection(node: dict, state: State) -> str:
    print_header()
    print(BLUE + "  💡 Reflection" + RESET)
    print()
    slow_print("  " + node["text"].replace("\n", "\n  "), delay=0.015)
    print()
    input(DIM + "  Press Enter when ready..." + RESET)
    return node["next"]


def handle_question(node: dict, state: State) -> str:
    print_header()

    # Axis label
    axis_labels = {
        "locus":        "Axis 1 — Agency",
        "contribution": "Axis 2 — Contribution",
        "radius":       "Axis 3 — Radius of Concern"
    }
    if node.get("axis"):
        print(DIM + f"  {axis_labels.get(node['axis'], node['axis'])}" + RESET)
        print()

    # Question text
    slow_print("  " + BOLD + WHITE + node["text"].replace("\n", "\n  ") + RESET, delay=0.012)
    print()

    options = node["options"]
    for i, opt in enumerate(options, 1):
        print(f"  {CYAN}{i}{RESET}. {opt['label']}")
    print()

    # Get valid input
    while True:
        try:
            raw = input(DIM + "  Your choice (number): " + RESET).strip()
            choice = int(raw)
            if 1 <= choice <= len(options):
                break
            print(f"  Please enter a number between 1 and {len(options)}.")
        except (ValueError, KeyboardInterrupt):
            print("  Please enter a number.")

    selected = options[choice - 1]

    # Record answer and signal
    state.answers[node["id"]] = selected["label"]
    if selected.get("signal"):
        state.record_signal(selected["signal"])

    print()
    print(DIM + f"  ✓ Got it." + RESET)
    time.sleep(0.4)

    return selected["next"]


def handle_decision(node: dict, state: State) -> str:
    """Route based on dominant signal — invisible to employee."""
    axis = node["axis"]
    dom = state.resolve_dominant(axis)

    for route in node["routes"]:
        if route["when"] == dom:
            return route["then"]

    # Fallback — find 'tied' route or first route
    for route in node["routes"]:
        if route["when"] == "tied":
            return route["then"]
    return node["routes"][0]["then"]


def handle_summary(node: dict, state: State) -> str:
    print_header()
    print(PURPLE + BOLD + "  📋 Today's Reflection" + RESET)
    divider(color=PURPLE)
    print()

    # Resolve all axes
    locus_dom        = state.axis_dominant.get("locus",        state.resolve_dominant("locus"))
    contribution_dom = state.axis_dominant.get("contribution", state.resolve_dominant("contribution"))
    radius_dom       = state.axis_dominant.get("radius",       state.resolve_dominant("radius"))

    # Axis labels for display
    locus_display = {
        "internal": "Victor  (internal agency)",
        "external": "Victim  (external locus)",
        "tied":     "Mixed   (both internal and external)"
    }
    contribution_display = {
        "giving":       "Contribution  (you gave)",
        "entitlement":  "Entitlement   (you tracked what came back)",
        "tied":         "Mixed         (both giving and tracking)"
    }
    radius_display = {
        "self":         "Self          (close-in frame)",
        "narrow":       "Narrow        (you + one other)",
        "wide":         "Wide          (team in view)",
        "transcendent": "Transcendent  (beyond yourself)",
        "tied":         "Mixed"
    }

    print(f"  {DIM}Agency      →{RESET}  {WHITE}{locus_display.get(locus_dom, locus_dom)}{RESET}")
    print(f"  {DIM}Contribution→{RESET}  {WHITE}{contribution_display.get(contribution_dom, contribution_dom)}{RESET}")
    print(f"  {DIM}Radius      →{RESET}  {WHITE}{radius_display.get(radius_dom, radius_dom)}{RESET}")
    print()
    divider()
    print()

    # Pick the right summary reflection
    # Map radius to two-pole for key lookup
    radius_key = "self" if radius_dom in ("self", "tied") else radius_dom
    if radius_dom == "tied":
        radius_key = "self"

    locus_key = locus_dom if locus_dom != "tied" else "external"
    contrib_key = contribution_dom if contribution_dom != "tied" else "entitlement"

    key = f"{locus_key}+{contrib_key}+{radius_key}"
    reflections = node.get("summary_reflections", {})
    summary_text = reflections.get(key, "Every day has something worth noticing. You showed up, and that's the start.")

    slow_print("  " + summary_text, delay=0.016)
    print()
    divider()
    print()

    # Closing question keyed to locus
    closing_questions = node.get("closing_questions", {})
    closing = closing_questions.get(locus_key, "What's one thing tomorrow you want to do differently?")
    print(GREEN + "  One question for tomorrow:" + RESET)
    print()
    slow_print("  " + BOLD + closing + RESET, delay=0.020)
    print()

    input(DIM + "  Press Enter to close..." + RESET)
    return node["next"]


def handle_end(node: dict, state: State) -> None:
    print_header()
    slow_print("  " + GREEN + node["text"] + RESET, delay=0.025)
    print()
    time.sleep(1)


# ─── Main Walker ──────────────────────────────────────────────────────────────

HANDLERS = {
    "start":      handle_start,
    "bridge":     handle_bridge,
    "reflection": handle_reflection,
    "question":   handle_question,
    "decision":   handle_decision,
    "summary":    handle_summary,
    "end":        handle_end,
}


def run(tree_path: str):
    nodes = load_tree(tree_path)
    state = State()
    current_id = "START"

    while current_id is not None:
        node = nodes.get(current_id)
        if not node:
            print(f"\nError: node '{current_id}' not found in tree.")
            sys.exit(1)

        handler = HANDLERS.get(node["type"])
        if not handler:
            print(f"\nUnknown node type: {node['type']}")
            sys.exit(1)

        result = handler(node, state)

        if node["type"] == "end":
            break

        current_id = result


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Find the tree file — look next to this script, or in a /tree subfolder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "reflection-tree.json"),
        os.path.join(script_dir, "..", "tree", "reflection-tree.json"),
        os.path.join(script_dir, "tree", "reflection-tree.json"),
    ]

    tree_path = None
    for c in candidates:
        if os.path.exists(c):
            tree_path = c
            break

    if not tree_path:
        print("Could not find reflection-tree.json.")
        print("Place it in the same folder as this script, or in a /tree subfolder.")
        sys.exit(1)

    try:
        run(tree_path)
    except KeyboardInterrupt:
        print("\n\n  Session ended early. See you tomorrow.\n")
        sys.exit(0)
