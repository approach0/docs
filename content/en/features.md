## Features
* Fast and effective math search, built on top of [a state-of-the-art formula retrieval model](http://ecir2019.org/best-paper-awards).
* Being able to cache on-disk index and specify the memory usage limit.
* Compressed and compact on-disk math index. Both in-memory and on-disk indices use specially designed compression schema and apply skip-list to boost search performance.
* Spceialized dynamic pruning strategy for amazing math-aware structural search efficency.
* Chinese tokeniser available, multi-bytes awareness from the beginning of design.
* Fulltext search is based on Indri project (C++), mature and fast.
* Memory leakage checked, search daemon has zero unfree.
* Robust TeX parser to convert user created math content to search-optimized representation.
* Math commutative rules awareness.
* Math symbol alpha-equivalence awareness.
* Term proximity awareness.
* Search results highlight.
* Scalable to multiple nodes across many machines.
