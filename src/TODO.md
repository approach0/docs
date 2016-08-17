## TODO
Listed are plans/directions the project is going to do
in the next stage.

### Top priority:
* indicate TeX grammar error in search result returned by searchd.
* math on-disk posting file compression
* math index on a filesystem that does not restrict number of inodes.
* search earily termination (depends on how many items has been evaluated).
* breadth-first dir-merge
* score: frequency & [sub\_expr depth > score (mnc\_score / search\_depth) > n\_lr\_paths]
* top level AND merge does not work
* oprtr decompose (when no search result is found)
* malloc hook / valgrind check
* Traffic stat / query log

### Want to implement
* search: concept search (horse == Pony)
* spell checking & 3-gram input suggestion
* query correction ("do you mean XXX")

### Do it when time is allowed
* faster Chinese tokenizer
* faster math-index/subpath-set
* in mnc\_score, compare father-to-root hash
* efficient postmerge
