import json
import ijson

with open("large-file.json", "r", encoding="UTF-8") as f:
    data = json.load(f)

user_to_repos = {}
for record in data:
    user = record["actor"]["login"]
    repo = record["repo"]["name"]
    if user not in user_to_repos:
        user_to_repos[user] = set()
    user_to_repos[user].add(repo)

print(user_to_repos)


iuser_to_repos = {}

with open("large-file.json", "r", encoding="UTF-8") as f:
    for record in ijson.items(f, "item"):
        user = record["actor"]["login"]
        repo = record["repo"]["name"]
        if user not in iuser_to_repos:
            iuser_to_repos[user] = set()
        iuser_to_repos[user].add(repo)

print(iuser_to_repos)
