#!/usr/bin/env python3
"""OKF knowledge-bundle experiment: with vs without bundle on small local models.

Fixture mirrors small-models.json: ollama /api/generate, temp 0.1,
num_predict 200, num_ctx 8192, think disabled. One-shot turns, no history.
Writes results.jsonl (every answer) + results.json (aggregate) into the
folder containing this script, and prints a line per completed run.
"""
import json, pathlib, sys, time, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
BUNDLE = HERE / "bundle"
ENDPOINT = "http://127.0.0.1:11434/api/generate"

WITHOUT_SYS = (
    "You are a research assistant answering a colleague's question. "
    "Answer concisely and precisely. If you do not know the answer, say you "
    "do not know rather than guessing."
)
WITH_SYS = (
    "You are a research assistant. A knowledge bundle is attached below inside "
    "<knowledge> tags. Answer the question using ONLY the information in the "
    "bundle. Do not use any prior knowledge. If the bundle does not contain "
    "the answer, reply exactly: Not in bundle.\n\n<knowledge>\n{bundle}\n</knowledge>"
)

def load_bundle():
    parts = []
    for rel in ["index.md", "concepts/okf-overview.md", "concepts/v01-fields.md",
                "concepts/v02-trust.md", "concepts/structure.md",
                "concepts/attested-computation.md"]:
        p = BUNDLE / rel
        parts.append(f"### {rel}\n\n{p.read_text().strip()}")
    return "\n\n".join(parts)

def call(model, system, prompt, options):
    payload = {
        "model": model, "system": system, "prompt": prompt,
        "stream": False, "options": options,
        "keep_alive": "30m",
    }
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode())

def main():
    cfg = json.loads((HERE / "questions.json").read_text())
    options = dict(cfg["fixture"]); options.pop("engine", None); options.pop("date", None); options.pop("host", None)
    bundle = load_bundle()
    jl_path = HERE / "results.jsonl"
    log_path = HERE / "answers.md"
    with jl_path.open("a") as jl, log_path.open("a") as lg:
        for model in cfg["models"]:
            for cond in cfg["conditions"]:
                sys_prompt = WITH_SYS.format(bundle=bundle) if cond == "with" else WITHOUT_SYS
                for qi, item in enumerate(cfg["questions"], 1):
                    t0 = time.time()
                    answer = ""
                    for attempt in (1, 2, 3):
                        try:
                            resp = call(model, sys_prompt, item["q"], options)
                            answer = resp.get("response", "").strip()
                            if answer:
                                break
                            print(f"empty resp {model}/{cond}/{item['id']} attempt {attempt}, retrying", flush=True)
                        except Exception as e:
                            if attempt == 3: raise
                            print(f"retry {model}/{cond}/{item['id']}: {e}", flush=True)
                        time.sleep(5)
                    dt = time.time() - t0
                    rec = {
                        "model": model, "condition": cond, "question_id": item["id"],
                        "seconds": round(dt, 1),
                        "eval_count": resp.get("eval_count"),
                        "prompt_eval_count": resp.get("prompt_eval_count"),
                        "answer": answer,
                    }
                    jl.write(json.dumps(rec) + "\n"); jl.flush()
                    lg.write(f"## {model} / {cond} / {item['id']}  ({dt:.1f}s)\n\n{item['q']}\n\n{answer}\n\n---\n")
                    lg.flush()
                    print(f"{model} {cond} {item['id']} {dt:.1f}s {resp.get('eval_count')} tok", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
