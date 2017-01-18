## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* math on-disk posting file compression
* math posting cache into memory
* AND > OR: one math tex maps to only one top-level posting
* binary search index for symbolic match such that 1/2016 will also find exact match (currently frequent terms such as 1/24 can return exact matches)
* math query decompose
* math query transform

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
* Mathquill add \qvar support
* return informative msg on query TeX parse error
