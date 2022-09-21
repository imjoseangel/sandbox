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
    GIT->>GIT: Pre-Commit
    Script->>Script: Static Code Analysis
    Script->>Continuous Integration: Pull Request
    Script->>Server: It works Faster!
    Server-->>GIT: Automated!
```

### The fourth stage - Realizing there is a long way to go

With Continuous Integration the process changes dramatically. The teams start to look for new automation techniques and think about changing their scripts for standard tools like *Terraform*, *Pulumi*, *Ansible* or *Chef* among others. Using a tool like *Terraform* doesn't mean that the team will improve their process. Compared with using Bash, the *Terraform* code is just another script launched from the local machine.

**Speed** is becoming an important asset and, the referred external tools help to achive it. Most of these tools are prepared to run different jobs in parallel.

**Security** is key and with standard tools it is possible to do **Static Security Analysis** before running the deployments.

**Refactoring** is a new word and it becomes part of the process. The team knows that is time to review and learn.

*Git* is now the standard and the Pull Request Process is improving. The team starts to implement other testing and quality gates before the approvals.

```mermaid
sequenceDiagram
    autonumber
    GIT->>as Code Tool: Manual Pipeline
    GIT->>GIT: History and Rollback
    GIT->>GIT: Pre-Commit
    as Code Tool->>as Code Tool: Static Code Analysis
    as Code Tool->>as Code Tool: Static Security Analysis
    as Code Tool->>as Code Tool: Refactor
    as Code Tool->>Continuous Integration: Pull Request
    Continuous Integration ->> Continuous Integration: Quality
    as Code Tool->>Server: It works!
    Server-->>GIT: Automated!
```

### Continuous Delivery is knocking the door
