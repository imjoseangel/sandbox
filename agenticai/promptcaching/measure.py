import json
import re
import time
import urllib.request

from traffic import TRAFFIC


def call(prompt):
    body = json.dumps(
        {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 50, "temperature": 0},
        }
    ).encode()
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    started = time.time()
    answer = json.loads(urllib.request.urlopen(request).read())["response"].strip()
    return answer, time.time() - started


def normalise(prompt):
    """Strip the parts that change and keep the part that matters."""
    question = prompt.split("Question:")[-1].lower().strip()
    question = re.sub(r"[^a-z0-9 ]", "", question)
    return re.sub(r"\s+", " ", question)


def run(key_of):
    cache, hits, spent = {}, 0, 0.0
    for prompt in TRAFFIC:
        key = key_of(prompt)
        if key in cache:
            hits += 1
            continue
        answer, took = call(prompt)
        cache[key] = answer
        spent += took
    return hits, len(TRAFFIC) - hits, spent


print(f"  {'strategy':26s}{'cache hits':>12s}{'model calls':>13s}{'seconds':>10s}")
for key_of, label in [
    (lambda p: p, "exact match on prompt"),
    (normalise, "exact match, normalised"),
]:
    hits, calls, spent = run(key_of)
    print(f"  {label:26s}{hits:>9}/{len(TRAFFIC)}{calls:>13}{spent:>9.1f}s")
