## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Demanding
* Prefix model **completeness**: wildcard, multi-math, mixed-query support.
* [✓] Prefix model efficiency: MaxScore-like **pruning**.
* Ad-hoc **boolean** query language support (must, should, must-not).
* **independent text search engine** (now Approach0 depends on Indri for text search, their code is overly complex and frequently breaks (in ArchLinux, crashes))
* Semantics
  * Operator/path latent space (math **topics**) or **operators** (sum, integral, factorial, fraction etc.) coverage.
  * **Text entity** search.
* [✓] Operand match **highlight**.
* Show last update of index at homepage.

### Future structure direction
* Clustering (using MPI?)
* Field search.
* Multi-threading

### Interface and Human interaction
* [✓] New interface (more intuitive to differentiate math and non-math mode input to users) and hand-written math pad.
* QAC, spelling correction, search suggestion. (Integrating text and math)

### Others
* faster Chinese tokenizer
* FIX: top level AND merge does not work
* Return informative msg on query TeX parse error
* Stats, query log
* indexing automation
* Special posting list for symbolic match such as "1/2016" and "\beta".
* Query transform for math equivalence (e.g. 1+1/n = (1+n)/n ), query expansion (e.g., \left| a + b \right| += | a + b| )
* Embedding and entity (e.g., pythagorean == x^2 + y^2 = z^2, horse == Pony)

### Consider additional indexing sources
We are planing to include other indexing sources aside from Math Stackexchange, listed below are some website we are considering to include in the future:
* artofproblemsolving.com
* matheducators.stackexchange.com
* MathOverflow
* CrossValidated
* physics stackexchange
