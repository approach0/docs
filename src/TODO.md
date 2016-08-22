## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* Demo provides a math symbol/function selection UI
* Search process timing and bottleneck analyze
* math on-disk posting file compression
* breadth-first dir-merge
* search earily termination (depends on how many items has been evaluated).
* math index on a filesystem that does not restrict number of inodes.
* malloc hook / valgrind check
* tune \qvar

### Want to implement
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
