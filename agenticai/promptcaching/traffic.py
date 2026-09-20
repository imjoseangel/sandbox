QUESTIONS = [
    "Why is my pod stuck in CrashLoopBackOff?",
    "Why is my pod stuck in CrashLoopBackOff?",
    "why is my pod stuck in crashloopbackoff?",
    "Why is my pod stuck in CrashLoopBackOff?  ",
    "My pod keeps restarting, what should I check?",
    "What does exit code 137 mean?",
    "What does exit code 137 mean?",
    "what does exit code 137 mean",
    "How do I drain a node safely?",
    "How do I drain a node safely?",
    "How do I safely drain a node?",
    "How do I rotate a database password?",
    "What does exit code 137 mean?",
    "Why is my pod stuck in CrashLoopBackOff?",
    "How do I drain a node safely?",
]


def wrap(question, i):
    """Real prompts are rarely just the question."""
    return (
        f"[request {1000 + i}] [2026-08-31T09:{i:02d}:00Z]\n"
        f"You are a Kubernetes support assistant.\n\n"
        f"Question: {question}"
    )


TRAFFIC = [wrap(question, i) for i, question in enumerate(QUESTIONS)]
