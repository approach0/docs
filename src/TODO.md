## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* pressure test (QPS)
* fix term query `\qvar{x} = \ln (1+X_t^2)+ \qvar{y}` crash
* https://approach0.xyz/search/?q=all%20positive%20integers%2C%20%24i%5E5%20%2B%20j%5E6%20%3D%20k%5E7%24&p=5 crash

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
