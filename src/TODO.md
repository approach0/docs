## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Demanding
* **Multi-math keywords** support under new model (re-entrant posting list iterators).
* Increase cache postlist hit chance by caching only long posting lists.
* **boolean** query language support (must, should, must-not).
* tag field index? (index and search MSE tag for example)
* eliminate the impact of sup/subscripts in some cases, e.g., definite and indefinite integrals.
* Show last update of index, and some visit statistics at homepage.
* handwritten, picture input UI interface.
* **faster indexer**
* [✓] **Combined math and text search** under new model.
* [✓] Operand match **highlight**.
* [✓] **Wildcard** under new model.
* [✓] Prefix model efficiency: MaxScore-like **pruning**.
* [✓] Path **operators hashing** to distinguish operator symbols.

### Future direction
* Scalability (using MPI?)
* Field search.
* QAC, spelling correction, search suggestion.

### Misc
* faster Chinese tokenizer
* Return informative msg on query TeX parse error.
* indexing automation.
* Special posting list for big number exact match, e.g., "1/2016".
* Semantics
  * math equivalence awareness, e.g. 1+1/n = (1+n)/n.
  * **Text synonym** awareness, e.g. horse = pony.
  * Embedding of both text and math, e.g. pythagorean == x^2 + y^2 = z^2

### Consider additional indexing sources
* artofproblemsolving.com
* matheducators.stackexchange.com
* MathOverflow
* CrossValidated
* physics stackexchange
