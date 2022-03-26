# octodns-verifier

 * `config/expected.yaml` contains a set of entries that we expect to match.
 * `config/branch.yaml` contains a proposed set of changes that we expect not to match.
 * `verify` is a placeholder script.

Run as:

```bash
usage: verify [-h] --config CONFIG --domain DOMAIN --nameserver NAMESERVER

./verify -c config/branch.yaml -d dns-exercise.dev -n ns-179.awsdns-22.com
```
