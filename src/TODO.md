## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* query GET URL
* copy-paste TeX to query input box.
* return informative msg on query TeX parse error
* normalize math-score to similar number range of term-score.
* Demo provides a math symbol/function selection UI
* Search process timing and bottleneck analyze
* math on-disk posting file compression
* breadth-first dir-merge

* search earily termination (depends on how many items has been evaluated).

### Want to implement
* query expansion, e.g. \left| a + b \right| +==> | a + b| 
* search: concept search (horse == Pony)
* spell checking & 3-gram input suggestion
* query correction ("do you mean XXX")

### Do it when time is allowed
* distributive search
* faster Chinese tokenizer
* faster math-index/subpath-set
* in mnc\_score, compare father-to-root hash
* efficient postmerge
* top level AND merge does not work
* write a script to extract traffic stat from query log
* improve score schema, consider:
	frequency & [sub\_expr depth > score (mnc\_score / search\_depth) > n\_lr\_paths]
* Demo UI should remind user if they are inputting math in a non-math mode.
* Github WEB hook, auto update demo on code changes (webhook for docs is done, but webhook for compile may need extra work such as using zmq/zeromq)
* KaTeX add \qvar support
