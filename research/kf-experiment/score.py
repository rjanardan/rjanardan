#!/usr/bin/env python3
"""Score the OKF bundle experiment from answers.md.

Rubric: per-question keyword sets (case-insensitive). A keyword 'hits' if it
appears in the answer. Report hits per question plus a coarse grade:
  grade 2 = all core keywords hit; 1 = core partially hit; 0 = none/misleading.
The grade is a machine aid; the human read in the guide is authoritative.
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent

RUBRIC = {
    "q1": {
        "core": ["google cloud", "june", "2026", "llm-wiki", "karpathy"],
        "extra": ["vendor-neutral", "markdown", "portable"],
    },
    "q2": {
        "core": ["type", "title", "description", "resource", "tags", "timestamp"],
        "extra": ["required"],
    },
    "q3": {
        "core": ["sources", "generated", "verified", "stale_after", "unverified",
                 "machine-confirmed", "human-reviewed"],
        "extra": ["status"],
    },
    "q4": {
        "core": ["index.md", "log.md", "markdown", "link", "graph"],
        "extra": ["concept", "entry", "changelog"],
    },
    "q5": {
        "core": ["runtime", "parameters", "executor", "attester", "receipt",
                 "deterministic"],
        "extra": ["no llm", "verdict", "gate"],
    },
}

def parse():
    text = (HERE / "answers.md").read_text()
    blocks = re.split(r"^## ", text, flags=re.M)[1:]
    runs = []
    for b in blocks:
        head, _, rest = b.partition("\n")
        m = re.match(r"(\S+) / (without|with) / (q\d)\s+\(([\d.]+)s\)", head.strip())
        if not m:
            continue
        model, cond, qid, secs = m.groups()
        body = rest.strip()
        runs.append({"model": model, "condition": cond, "question_id": qid,
                     "seconds": float(secs), "answer": body})
    return runs

def grade(run):
    a = run["answer"].lower()
    r = RUBRIC[run["question_id"]]
    core_hits = sum(1 for k in r["core"] if k in a)
    extra_hits = sum(1 for k in r["extra"] if k in a)
    if core_hits == len(r["core"]):
        g = 2
    elif core_hits >= max(2, len(r["core"]) // 2):
        g = 1
    else:
        g = 0
    return g, core_hits, extra_hits, len(r["core"]), len(r["extra"])

def main():
    runs = parse()
    print(f"parsed {len(runs)} runs\n")
    order = ["qwen3:1.7b", "qwen3:4b", "gemma4:e4b"]
    for model in order:
        for cond in ("without", "with"):
            row = [r for r in runs if r["model"] == model and r["condition"] == cond]
            row.sort(key=lambda r: r["question_id"])
            cells, secs = [], 0
            for r in row:
                g, ch, eh, ncore, nextra = grade(r)
                cells.append(f"{g}({ch}/{ncore})")
                secs += r["seconds"]
            print(f"{model:12s} {cond:7s} " + "  ".join(f"{r['question_id']}:{c}" for r, c in zip(row, cells)) + f"   total_secs={secs:.0f}")
    print("\nkeyword detail:")
    for model in order:
        for cond in ("without", "with"):
            for r in runs:
                if r["model"] == model and r["condition"] == cond:
                    g, ch, eh, ncore, nextra = grade(r)
                    hits = [k for k in RUBRIC[r["question_id"]]["core"] if k in r["answer"].lower()]
                    miss = [k for k in RUBRIC[r["question_id"]]["core"] if k not in r["answer"].lower()]
                    print(f"{model} {cond} {r['question_id']}: hit={hits} miss={miss} len={len(r['answer'])}")

if __name__ == "__main__":
    main()
