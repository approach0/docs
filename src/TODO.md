## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Demanding
* Show informative msg on query **TeX parse error**.
* **boolean** query language support (must, should, must-not).
* **Field search** (e.g., search MSE tag).
* ~~v3 **wildcards** support?~~
* [✓] initial threshold, update documentation.
* [✓] recognize query string when no **comma separated**.
* [✓] lower search granularity to sector tree.
* [✓] merge CONST and VAR tokens.
* [✓] different symbol weight: Math token > math variable > sub/sup-script.
* [✓] on-disk math index compression, faster indexer, index-stage init threshold.
* [✓] Re-design representation:
  * [✓] eliminate the impact of sup/subscripts in some cases, e.g., definite and indefinite integrals. 
  * [✓] And also prime variable, e.g., x and x'.
  * [✓] being able to differentiate `$\sum_{i=0}^n x_i = x$` and `$\sum_{i=0} x_i^n = x$`. 
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
* picture input UI interface on mobile platform, picture input.
* faster Chinese tokenizer
* QAC, spelling correction, search suggestion.
* Semantics
  * math equivalence awareness, e.g. 1+1/n = (1+n)/n.
  * **Text synonym** awareness, e.g. horse = pony.
  * Embedding of both text and math, e.g. pythagorean == x^2 + y^2 = z^2

### Consider additional indexing sources
* [✓] Math StackExchange
* [✓] artofproblemsolving.com
* [Proof wiki](https://proofwiki.org/wiki/Main_Page)
* https://brilliant.org/
* PlanetMath
* CrossValidated
* physics stackexchange
* matheducators.stackexchange.com
* MathOverflow
* Wolfram MathWorld
* Wikipedia (English version)
* Socratic
* NIST DLMF
