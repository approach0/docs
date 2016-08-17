## Features
* Math search with punning method, efficient for large scale corpus.
* Posting lists can be configured to cache into memory (you can specify
the size), using FOR delta-encode, and skip-list data structure.
* Compact index, small indices size.
* Chinese tokeniser available, multi-bytes awareness from the beginning
of design.
* Fulltext index writer/reader is based on Indri project (C++), other
parts are mostly written from scratch in C. Why? Fast, simple and downright.
Anyway, it is reinventing the wheel. I know!
* Robust TeX parser, handles most user-created math content from
math.stackexchange.com correctly.
* Math commutative rules awareness.
* Math symbol alpha-equivalence awareness.
* BM25 Okapi scoring schema in fulltext part.
* Proximity search using efficient "minDist" measurement.
* Search results highlight.

Special thanks to [yzhan018](https://github.com/yzhan018") who
submits the initial FOR-delta implementation. This project is made public
just hoping someone can feel the usefulness, send some feedbacks (to Github
issue page), or contribute in any form.
