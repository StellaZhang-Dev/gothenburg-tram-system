# Lab 3 Peer Review

**Reviewing group:** 148
**Submitting group:** 106

This review is based on (1) a live demonstration of the application running on the submitting group’s machine, and (2) inspection of the code provided by the submitting group (with particular focus on the main path computation/visualization logic).

## Section 1: Core functionality

### Does the application run? (yes/no)

**Yes.**
During the live demonstration, the web application started successfully and the main pages were accessible. Route queries could be submitted and results were displayed without crashes. Furthermore, during the presentation, users could click on corresponding stations to obtain more detailed information about that station. This adds to the usability of the interface and makes the web application feel more interactive.

### Does the application display the complete map of tram lines? (yes/no)

**Yes.**
The application displays the tram network map in the UI. The submitting group also explained that they regenerated/updated the SVG map by collecting stop information (including Västtrafik stop identifiers) and replacing the original SVG with a newly generated one. This suggests the displayed map is intended to cover the full network rather than a partial subset. This shows a clear effort to go beyond the minimal requirements and improve the realism of the visualization. This work also shows a mature understanding of how data preprocessing can improve downstream visualization.

### Is it possible to query shortest path between any two points? (yes/no)

**Yes (for valid stop inputs).**

The system supports querying routes between two stops via the web UI and returns both:

- a **quickest** path (time-based), and
- a **shortest** path (distance-based).

In the implementation, two Dijkstra runs are performed with different cost functions:

- `dijkstra(..., cost=lambda u,v: specialized_transition_time(...))`
- `dijkstra(..., cost=lambda u,v: specialized_geo_distance(...))`

The returned routes are then post-processed and displayed as text, and the SVG is recolored accordingly. Distinct color boundaries made route directions easily discernible through color alone. This is particularly helpful for users when comparing the two routes at a glance.

### Does the application deal with changes correctly? (yes/no)

**Yes.**
The submission explicitly models line changes by using a specialized graph where nodes are `(stop, line)` tuples. In the displayed route strings, the line number is shown when the line changes. This is implemented by tracking the current line in `show_shortest()` and inserting the line label when `node[1]` changes.

Additionally, the specialized graph includes “change edges” between different line-nodes for the same stop. This supports transfer behavior in principle.

### Does the application show current traffic information? (yes/no)

**Yes (under a broader interpretation) / No (based on application-internal display).**

under a broader interpretation that includes providing access to authoritative real-time traffic information via external sources, the application can be considered to satisfy this requirement. In particular, the system supports linking from stops to external Västtrafik pages (via stop Gids), where up-to-date traffic information is available.

However, Under a strict interpretation of “showing current traffic information” as presenting live traffic state (e.g. delays, cancellations, disruptions) directly within the application UI, this criterion is assessed as **No**, since the application itself relies on static network data for route computation.

### Does the application correctly handle invalid input? (yes/no)

**Yes (under an exception-based validation standard) / Limited (from a UI-level validation perspective).**

Under a functional interpretation aligned with the assignment requirements, the application correctly handles invalid input by using exception-based validation in the view layer. In particular, `NodeNotFound` and `KeyError` exceptions are caught and translated into appropriate HTTP 400 responses, which prevents server crashes and provides meaningful feedback to the user. From this perspective, the requirement for handling invalid input is satisfied.

From a stricter UI- and design-oriented perspective, input validation is not performed explicitly before route computation, but instead relies on downstream exceptions. While this approach is functionally correct, it may be considered less explicit in terms of validation flow and user-facing clarity. The “Limited” assessment therefore reflects a stylistic or architectural preference for earlier, front-loaded validation, rather than a deficiency in correctness or assignment compliance.


## Section 2: Code quality

This section comments on code structure, reuse of graph abstractions, and whether the shortest-path logic follows the intended “single Dijkstra + varying cost function” pattern.

### Reuse of Lab 2 code (interface and structure)

From inspection of the submitted code, the tram network is implemented as a subclass of `WeightedGraph`, and shortest-path computation is performed using a `dijkstra()` function imported from the graphs module. This indicates an architectural approach consistent with the assignment: using graph abstractions as the foundation for the tram network.

While the internal correctness of the original Lab 2 implementation cannot be fully assessed from this review alone, the interface usage pattern (graph subclass + Dijkstra calls) suggests a structured attempt to build Lab 3 on top of earlier graph components.

### Use of `dijkstra()` as intended

**Yes.**

The submission uses a single Dijkstra implementation and applies different cost functions to compute:

- quickest paths (transition time), and
- shortest paths (geographical distance).

This matches the intended design: different metrics are obtained by changing the cost function, without duplicating shortest-path algorithm code.

### Strengths in structure and readability

- The code is divided into clear responsibilities:
  - loading the tram network from JSON (`readTramNetwork`)
  - building a specialized graph to incorporate line changes (`specialize_stops_to_lines`)
  - providing metric-specific costs (`specialized_transition_time`, `specialized_geo_distance`)
  - producing UI-facing outputs and SVG coloring (`show_shortest`)
- The route text output includes line numbers and line changes, aligning with the assignment’s example output.

### Points for improvement (robustness and maintainability)

1. **Global computation at import time**

   - The submission defines:

     ```python
     network = specialize_stops_to_lines(readTramNetwork())
     ```

     at module scope. This means the network is built when the module is imported, rather than per-request or via a controlled initialization. In Django, this can lead to:

     - slower startup,
     - difficulty reloading data during development,
     - and potential issues if files/paths differ between environments.
2. **Path handling and assumptions**

   - The code does:

     ```python
     quickest.pop(0)
     shortest.pop(0)
     ```

     This assumes the first element is always a placeholder/start node that should be removed. This may work for the current graph construction, but is fragile if the path format changes.
3. **Cost functions treat missing attributes as change penalties**

   - In `specialized_transition_time`, the logic:

     ```python
     time = spec_network[a][b].get("time")
     if not time:
         return changetime
     return time
     ```

     treats `time=0` as “missing” (because `0` is falsy). This makes all zero-time edges (e.g., change edges) incur `changetime` penalty, which is likely intended, but it also means you must be careful that a real time of `0` would be treated as a change edge.
4. **Imports and module hygiene**

   - The code uses wildcard imports:

     ```python
     from .trams import *
     ```

     which can reduce readability and increase the chance of name conflicts.
   - There are multiple imports repeated later in the file (e.g., `os`, `settings`), which can be simplified.
5. **External path manipulation**

   - The submission modifies `sys.path` to locate `lab1-group-106` and imports `tramdata` from there.
   - While this can work locally, it can be brittle across different setups.

### UI consistency note (from demonstration)

During the demonstration and discussion, it was observed that some UI interactions (e.g., clicking on different stops) appeared to surface line-related contextual information with slight variation across stops. In particular, while the underlying functionality was present, the way contextual information was surfaced to the user (e.g. within the map or route display) appeared less uniform across interactions. This was noted as a minor presentation/UI observation rather than a functional issue.

## Section 3: Screenshots

The submitting group provided screenshots for inclusion in the peer-review submission:

1. **Screenshot 1:** Web application showing a computed route between two stops (with the map visible and a route result displayed).
2. **Screenshot 2:** Source code view of `show_shortest()`.

Both screenshots support the evaluation above.


## Overall assessment

Based on the live demonstration and code inspection, the submission fulfills the core requirements of Lab 3 and demonstrates a solid and well-structured implementation. The web application runs correctly, presents the tram network map, supports route queries, and computes shortest and quickest paths using a clean reuse of Dijkstra’s algorithm with different cost functions.

The handling of line changes, input validation, and traffic-related information reflects reasonable design choices that satisfy the assignment requirements. Where limitations are noted, they primarily concern presentation or UI-level clarity rather than functional correctness. These aspects do not detract from the overall quality or validity of the solution.

In conclusion, the submission is well-prepared, functionally correct, and clearly aligned with the intended learning outcomes of the assignment.
