import json
import urllib.request

import numpy as np

PAIRS = [
    (
        "Why is my pod stuck in CrashLoopBackOff?",
        "Why is my pod stuck in CrashLoopBackOff?",
        True,
    ),
    (
        "why is my pod stuck in crashloopbackoff",
        "Why is my pod stuck in CrashLoopBackOff?",
        True,
    ),
    (
        "My pod keeps restarting, what should I check?",
        "Why is my pod stuck in CrashLoopBackOff?",
        True,
    ),
    ("How do I safely drain a node?", "How do I drain a node safely?", True),
    # these look similar and mean different things
    (
        "How do I rotate a database password?",
        "How do I rotate a TLS certificate?",
        False,
    ),
    ("How do I scale up a deployment?", "How do I scale down a deployment?", False),
    ("What does exit code 137 mean?", "What does exit code 143 mean?", False),
    ("How do I drain a node?", "How do I cordon a node?", False),
]


def embed(texts):
    body = json.dumps({"model": "mxbai-embed-large", "input": texts}).encode()
    request = urllib.request.Request(
        "http://localhost:11434/v1/embeddings",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    return [
        d["embedding"]
        for d in json.loads(urllib.request.urlopen(request).read())["data"]
    ]


def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


scored = []
for new, cached, same in PAIRS:
    va, vb = embed([new, cached])
    scored.append((cosine(va, vb), new, same))

for score, question, same in sorted(scored, reverse=True):
    label = "same question" if same else "DIFFERENT question"
    print(f"  {score:+.3f}  {label:19s} {question[:40]}")

print(f"\n  {'threshold':>11s}{'correct hits':>15s}{'wrong answers served':>23s}")
for threshold in [0.70, 0.80, 0.85, 0.90, 0.95]:
    good = sum(1 for s, _, same in scored if same and s >= threshold)
    bad = sum(1 for s, _, same in scored if not same and s >= threshold)
    total = sum(1 for _, _, same in scored if same)
    print(f"  {threshold:>11.2f}{good:>12}/{total}{bad:>21}")
