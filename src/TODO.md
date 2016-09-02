## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* enlarge indices, pressure test (QPS)
* search earily termination (depends on how many items has been evaluated).
* a helpful guide page about how to use, what is indexed, some typical malformed TeX (e.g. `_()`, `\int bound input` and `sin`) with animated gif, wildcard, and where to put feedback/contribute (quiz-list, edit guide page). Also tell user to follow twitter on updates.
* Demo math rendering switch to MathJax (see https://approach0.xyz/search/?q=%24%5Clog%5Cleft(x%5E%7B-1%7D%5Cright)%24&p=1)

### Want to implement
* query expansion, e.g. \left| a + b \right| +==> | a + b| 
* search: concept search (horse == Pony)
* spell checking & 3-gram input suggestion
* query correction ("do you mean XXX")

### Do it when time is allowed
* math on-disk posting file compression
* math posting cache into memory
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
