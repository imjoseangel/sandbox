# What are your git aliases?

## Introduction

I've been requested multiple times about sharing my `.gitconfig` to copy my aliases.

I use git aliases for two reasons:

1. To improve productivity.
2. To remember interesting `git` commands and learn from them.

## My Gitconfig

These are my aliases included in my `~/.gitconfig` file for your reference:

```ini
[alias]
    a = add .
    aliases = config --get-regexp alias
    alias = ! git config --get-regexp ^alias\. | sed -e s/^alias.// -e s/\ /\ $(printf "\043")--\>\ / | column -t -s $(printf "\043") | sort -k 1
    ap = add . -p
    addups = remote add upstream
    bd = branch -d
    bi = bisect
    bl = branch -l
    blr = branch -a
    br = branch -r
    ca = commit -a
    cam = commit -a -m
    ci = commit -m
    cid = commit --author='imjoseangel <secondemail@example.com>' -m
    cm = commit
    co = checkout
    colast = checkout -
    comments = commit -m 📒Comments
    count = rev-list --count devel
    db = branch -D
    forgetAbout = rm --cached
    formatting = commit -m 💅Formatting
    fp = fetch -p
    grep = grep -F
    laf = fsck --lost-found
    last = log -1 HEAD
    latest = log -5 --pretty --oneline
    ls = ls-files --others --exclude-standard -z
    mend = commit --amend
    nb = checkout -b
    op = gc --prune=now --aggressive
    pdo = push -d origin
    pf = push --force-with-lease
    po = push origin
    pou = push --set-upstream origin
    pr = pull --rebase
    pror = remote prune origin
    prud = pull --rebase upstream devel
    prum = pull --rebase upstream main
    prune = remote update --prune
    ptag = push origin --tags
    ra = rebase --abort
    rc = rebase --continue
    refactor = commit -m 👷Refactor
    remotes = remote -v
    renb = branch -m
    rh = reset --hard
    rhh = reset --hard HEAD
    ri = rebase -i upstream/devel
    rim = rebase -i upstream/main
    rl = reflog
    rp = repack -ad
    s = status -s
    search = rev-list --all
    sh = show
    short = shortlog -sn
    sign = commit --amend --no-edit --signoff
    st = status
    stashes = stash list
    tests = commit --allow empty -m ✅Tests
    tuto = help tutorial
    tuto2 = help tutorial-2
    unstash = stash pop
    vc = clean -dfx
    wow = log --all --graph --decorate --oneline --simplify-by-decoration
```

Running `git alias` after adding to the `.gitconfig` shows the list of all the aliases as a reference list.

To get more info, just run `git help <command or alias>`. For instance:

```sh
git help st
'st' is aliased to 'status'
```

```sh
git help status
```

There are two aliases I find interesting for beginners:

```sh
git tuto
git tuto2
```

Try them and add your comments and suggestions with different approaches.
