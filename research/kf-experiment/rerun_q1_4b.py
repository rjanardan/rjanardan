#!/usr/bin/env python3
"""Rerun the single failed cell (qwen3:4b / without / q1) with a larger
token budget, replacing the empty-answer record. Run AFTER the main
experiment process exits so the 8 GB host is not serving two models at once.
"""
import json, pathlib, re, time, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ENDPOINT = "http://127.0.0.1:11434/api/generate"

WITHOUT_SYS = (
    "You are a research assistant answering a colleague's question. "
    "Answer concisely and precisely. If you do not know the answer, say you "
    "do not know rather than guessing."
)

def call(model, system, prompt):
    payload = {"model": model, "system": system, "prompt": prompt,
               "stream": False, "keep_alive": "30m",
               "options": {"temperature": 0.1, "num_predict": 1500,
                           "num_ctx": 8192, "think": False}}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode())

# 1. strip the failed empty block from answers.md and results.jsonl
am = HERE / "answers.md"; jl = HERE / "results.jsonl"
text = am.read_text()
pat = re.compile(r"^## qwen3:4b / without / q1.*?(?=^## |\Z)", re.S | re.M)
text2, n = pat.subn("", text)
am.write_text(text2)
print("answers.md blocks removed:", n)
lines = [l for l in jl.read_text().splitlines() if l.strip()]
kept = [l for l in lines if not (json.loads(l)["model"] == "qwen3:4b"
        and json.loads(l)["condition"] == "without"
        and json.loads(l)["question_id"] == "q1")]
jl.write_text("\n".join(kept) + ("\n" if kept else ""))
print("results.jsonl records removed:", len(lines) - len(kept))

# 2. run the cell again at a 1500-token budget
q = json.loads((HERE / "questions.json").read_text())
item = next(x for x in q["questions"] if x["id"] == "q1")
t0 = time.time()
resp = call("qwen3:4b", WITHOUT_SYS, item["q"])
dt = time.time() - t0
answer = resp.get("response", "").strip()
rec = {"model": "qwen3:4b", "condition": "without", "question_id": "q1",
       "seconds": round(dt, 1), "eval_count": resp.get("eval_count"),
       "prompt_eval_count": resp.get("prompt_eval_count"), "answer": answer,
       "note": "rerun at num_predict 1500 after empty 700-token attempts"}
jl.write_text(jl.read_text().rstrip("\n") + "\n" + json.dumps(rec) + "\n")
with am.open("a") as f:
    f.write(f"## qwen3:4b / without / q1  ({dt:.1f}s)  [rerun, 1500 budget]\n\n"
            f"{item['q']}\n\n{answer}\n\n---\n")
print(f"rerun complete: {dt:.1f}s, eval {resp.get('eval_count')} tok, answer_len {len(answer)}")
