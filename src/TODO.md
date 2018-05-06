## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Major features for next big version
* Clustering (using MPI?)
* Compressed, cached math posting list
* independent text search (Now we rely on Indri for text search, its code frequently breaks (in ArchLinux, crashes))
* Fuzzy search model, state-of-the-art accuracy (match subexpression in doc with subexpression in query)
* Being able to drop posting list (those prefix-paths who are too short) at merge runtime depeading on minheap value.
* General path matching score (except symbol, further consider depth, operator HASH)
* Special posting list for symbolic match such as "1/2016" and "\beta".
* math query transform, query expansion (e.g., \left| a + b \right| +==> | a + b| )
* Stats, query log
* indexing automation
* QAC, spelling correction, search suggestion. (Integrating text and math)
* New interface (more intuitive to differentiate math and non-math mode input to users) and hand-written math pad.
* Embedding and entity (e.g., pythagorean == x^2 + y^2 = z^2, horse == Pony)
* Query language (do we really want?)

### Others
* faster Chinese tokenizer
* FIX: top level AND merge does not work
* Return informative msg on query TeX parse error
