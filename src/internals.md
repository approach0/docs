## Internals
Some old papers/posters describe in detail what our search
methods are. You may find useful to read these resources first:

1. [ECIR16 Slides](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-OPMES-slides-handouts.pdf)
2. [ECIR16 Poster](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-Wei-Poster-publish.pdf)
3. [ECIR16 Paper](https://github.com/tkhost/tkhost.github.io/blob/master/opmes/ecir2016.pdf)
4. [My graduate thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf)

Although Approach0 is a complete rewrite based on previous
prototype (OPMES), the basic ideas of searching math expression
remain unchanged in both systems. Approach0 mainly makes an advance
in the following aspects on top of OPMES:

1. Combine math-only search with fulltext search
2. Adds some feature (e.g. math expression wildcards)
3. Better code framework

The data structure details of posting list are written in the next section,
other technical details are not included in this document, but you are welcome to request in project issue page for more specific technical issues.

## Posting list structure
There are two different posting lists, `math posting list` and `term posting list`. A `math posting list` is mapped from a path token from tree representation of a math expression, e.g. VAR/ADD/TIMES. A `term posting list` is mapped from a text word from dictionary. Both posting list is concatenation of posting list items.

The data structure for term posting list item is divided into on-disk and in-memory (cached) posting list.
Indri takes care of on-disk term posting list and approach0 just calls Indri's API to get posting list items when needed.

The in-memory posting list item for terms is defined like below (each square bracket is a 32-bit field):

[docID][TF][pos_1][pos_2]...[pos_TF]

The math posting list currently only has on-disk version, its posting list item looks like below:

[expID, n_lr_paths, n_paths], [docID], [pathInfo pointer]
where pathInfo points to another posting list that stores additional information array for that item:
[leaf_id], [subr_id], [lf_symbol] ... (repeating `n_paths` times)
