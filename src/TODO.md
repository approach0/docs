## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Demanding
* lower search granularity to sector tree.
* merge CONST and VAR tokens.
* different symbol weight: Math token > math variable > sub/sup-script.

`$$
\text{Score} = \sum_t \text{sf}_{t,d} \cdot \text{idf}_{t,d}  \\
\text{sf}_{t,d} = S{\text{sy}} \left( (1- \theta) + \theta \frac 1 {\log(1 + \operatorname{leaves}(T_d))} \right)  \\
\text{idf}_{t,d} = \sum{p \in \mathfrak{T}( M(t, d) )} \log \frac{N}{\text{df}_p}
$$`

* on-disk math index compression, faster indexer, index-stage init threshold.
* Re-design representation:
  * eliminate the impact of sup/subscripts in some cases, e.g., definite and indefinite integrals. 
  * And also prime variable, e.g., x and x'. 
  * being able to differentiate `$\sum_{i=0}^n x_i = x$` and `$\sum_{i=0} x_i^n = x$`. 
  * Solution: e.g., \sum lifted to operator, leaving a `base` to match variable, hanging there with sub/sup-scriptions.
* **boolean** query language support (must, should, must-not).
* Field search (index many sources and search MSE tag for example).
* [✓] put some large resources on CDN (jsdelivr.com)
* [✓] Show last update of index and some visit statistics at homepage.
* [✓] faster TeX rendering using mathjax v3.
* [✓] **Increase cache postlist hit chance** by caching only long posting lists.
* [✓] scalability: Multiple nodes on each core or different machines (using MPI)
* [✓] re-entrant posting list iterators and MNC scoring.
* [✓] **Combined math and text search** under new model.
* [✓] Operand match **highlight**.
* [✓] **Wildcard** under new model.
* [✓] Prefix model efficiency: MaxScore-like **pruning**.
* [✓] Path **operators hashing** to distinguish operator symbols.

### Misc
* picture input UI interface on mobile platform, handwritten input on PC.
* QAC, spelling correction, search suggestion.
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
* Wolfram MathWorld
* Wikipedia (English version)
* Socratic
* NIST DLMF
* https://brilliant.org/
* PlanetMath
* [Proof wiki](https://proofwiki.org/wiki/Main_Page)
