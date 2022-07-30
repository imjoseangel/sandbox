# List and Tuple

| Operation     | Example         | Complexity Class |
|---------------|-----------------|------------------|
| Index         | l[i]            | O(1)             |
| Store         | l[i] = 0        | O(1)             |
| Length        | len(l)          | O(1)             |
| Append        | l.append(5)     | O(1)             |
| Pop           | l.pop()         | O(1)             |
| Clear         | l.clear()       | O(1)             |
| Check ==, !=  | l == l2         | O(N)             |
| Insert        | l[a:b] = ...    | O(N)             |
| Delete        | del l[i]        | O(N)             |
| Containment   | x in/not in L   | O(N)             |
| Copy          | l.copy()        | O(N)             |
| Remove        | l. remove(...)  | O(N)             |
| Pop           | l.pop(i)        | O(N)             |
| Extreme Value | min(l) / max(l) | O(N)             |
| Reverse       | l.reverse()     | O(N)             |
| Iteration     | for v in l:     | O(N)             |
| Sort          | l.sort()        | O(N log N)       |
| Multiply      | k * l           | O(k N)           |
| Slice         | l[a:b]          | O(b-a)           |
| Extend        | l.extend(...)   | O(len(...))      |
| Construction  | list(...)       | O(len(...))      |
