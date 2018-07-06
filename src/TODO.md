## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Demanding
* Prefix model completeness: wildcard, multi-math, mixed-query support.
* Prefix model efficiency: drop unimportant prefix paths, skip items dynamically depending on minheap value.
* Multi-threading
* hightlight matches within expression.
* Ad-hoc boolean query language support (must, should, must-not).
* independent text search (Now we rely on Indri for text search, its code frequently breaks (in ArchLinux, crashes))
* Clustering (using MPI?)
* Operator similarity / Path weight (sum, integral is more important feature than add or times) / Path matched depth

### Interface and Human interaction
* QAC, spelling correction, search suggestion. (Integrating text and math)
* New interface (more intuitive to differentiate math and non-math mode input to users) and hand-written math pad.

### Others
* faster Chinese tokenizer
* FIX: top level AND merge does not work
* Return informative msg on query TeX parse error
* Stats, query log
* indexing automation
* Special posting list for symbolic match such as "1/2016" and "\beta".
* Query transform for math equivalence (e.g. 1+1/n = (1+n)/n ), query expansion (e.g., \left| a + b \right| += | a + b| )
* Embedding and entity (e.g., pythagorean == x^2 + y^2 = z^2, horse == Pony)
