## Features
* Fast and effective math search, built on top of [a state-of-the-art formula retrieval model](http://ecir2019.org/best-paper-awards).
* Being able to cache specified indicies into memory, with good compression and skip-list to boost search performance.
* Support wildcards query.
* Chinese tokeniser available, multi-bytes awareness from the beginning
of design.
* Fulltext search is based on Indri project (C++), mature and fast.
* Memory leakage checked, searchd zero unfree.
* Robust TeX parser, handles most user-created math content.
* Math commutative rules awareness.
* Math symbol alpha-equivalence awareness.
* Proximity search.
* Search results highlight.
* Being able to scale to multiple nodes across many machines.

Special thanks to people who have contributed to this project:
* [yzhan018](https://github.com/yzhan018) who submitted the initial FOR-delta implementation.
* [Sil](https://github.com/TheSil) who helped to create the cralwer script for AoPS website.
