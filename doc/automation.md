# From Local Scripts to Continuos Deployment - My Experience and Vision

## Introduction - Fail Fast and Teams

Many teams try to implement automated deployment for their applications or their Cloud components but most of them fall in the same hole: **Fail Fast** and consequently, **Confidence**.

There are different reasons that prevent a **Grow Mindset**, just the typical examples:

* Non-sense strict deadlines
* Lack of confidence
* Complain of Failure
* Judging performance
* Lack of innovation

### “Ever tried. Ever failed. No matter. Try Again. Fail again. Fail better.” - Samuel Beckett

Automation requires time to start, creativity, investigation and innovation. Failing fast is part of the learning process.

Think if the implemented process is *optimal and scalable*. Investigate for alternative solutions and improvements. With the right mindset to *refactor* the process and the code, every team will reach to their full potential.

## From Human Intervention to Full Automation

Let's define a possible timeline of how it could be the trip from manual run to a full automated process.

### The first stage - Fear of losing job

When a new technology knocks to the door, there are multiple reasons stopping a Team to progress on innovation and new techniques adoption.

* The *damned* comfort zone
* Lost one's job
* False sense of control

But don't worry, with the right coaching and time, teams will gain confidence and will improve aboves procedure.

With aboves feelings over the table, and other external factors, the best approach could be:

```mermaid
sequenceDiagram
    autonumber
    Local->>Script: Manual Run
    Script->>Server: It works!
    Server-->>Local: Automated!
```

It works, and it is automated but there is still some field for improvement.

### The second stage - Starting the Dunning-Kruger Effect

This is a wonderful stage, where the team start to gain confidence and is pretty damn sure they know a whole lot. On this stage, the automation starts to grow and the team starts to learn new techniques. They use *git* and *pipelines*.

```mermaid
sequenceDiagram
    autonumber
    GIT->>Script: Manual Pipeline
    GIT->>GIT: History and Rollback
    Script->>Server: It works!
    Server-->>GIT: Automated!
```

It seems similar to the *first stage* but not in the least. The process is:

* Centrallized in a Git repository.
* Runnable by anyone in the team.
* It has a history log.
* It can be rolled back and traced.

#### Using a CI/CD Tool with inline code

> **Warning!!!**
>
> Having all the logic in the pipeline or using graphical options is not recommended.
>
>It is not scalable, has a lot of dependency on the CI/CD tool and don't offer the advantages like the rollbacks, traces and logging given the *as code* options.
>
>It could be something like:

```mermaid
sequenceDiagram
    autonumber
    Note over CI/CD Tool: Inline Code
    CI/CD Tool->>Server: Manual Pipeline
    Server->>CI/CD Tool: It works!
```

### The third stage - Questioning our current solution

Hosting our code to Git is taking a firm step in the way of automation.

The curiosity starts to open new ways or working with Git like *Git Hooks*. The team discovers how to apply Continuous Integration in their code. The original scripts could be custom *Bash*, *Python* or *Powershell* and use *shellcheck*, *pylint* or *PSScriptAnalyzer* respectively. The **Pre-Commit**, **Static Analysis** and **Pull Requests** have arrive to stay.

```mermaid
sequenceDiagram
    autonumber
    GIT->>Script: Manual Pipeline
    GIT->>GIT: History and Rollback
    GIT->>GIT: Pre-Commit and CI
    Script->>Script: Static Analysis
    Script->>Continuous Integration: Static Analysis
    Script->>Server: It works!
    Server-->>GIT: Automated!
```
