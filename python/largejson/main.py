import json

with open("large-file.json", "r") as f:
    data = json.load(f)

user_to_repos = {}
for record in data:
    user = record["actor"]["login"]
    repo = record["repo"]["name"]
    if user not in user_to_repos:
        user_to_repos[user] = set()
    user_to_repos[user].add(repo)
