## Internals

### TeX Parser
TeX parser converts TeX to Operator Tree (or OPT) and leaf-root paths. There are many details involved, among them
* Each node in OPT will be assigned a ID in a way that leaf nodes always occupy lower space
* Each node in OPT will save its position [start, end] information from original TeX string
* Fingerprint (or `fp`) (the symbol hash digested from 4 nodes on top of a node) is generated for each leaf-root path
* A subtree Hash is generated for each subtree
* A pathID and a leafID (starting from 1) are generated for each path, initially they are the same
* Max pathID/leafID is also the maximum number of leaf-root paths here, they are no greater than MAX_SUBPATH_ID = 64
* Any *nil* node will be pruned
* Each *meaningful* internal node (non-meaningful are tokens like `T_BASE`, `T_SUBSCRIPT`, `T_SUPSCRIPT` or `T_NIL`) gets assigned a pathID which is the pathID from one of its descendant leaf child. Also, non-meaningful nodes are not counted when generating fingerprint.
* A rank number will be assigned to its children if a node is non-communitive node (such as fraction operator)

The following is an example output for expression `$a+b/c= $` (notice the RHS has nothing so it will reduce into *nil*)
```
Operator tree:
     └──(equal) #4, token=GTLS, subtr_hash=`38088', pos=[0, 5].
           └──(plus) #5, token=ADD, subtr_hash=`13388', pos=[0, 5].
                 │──(pos) #6, token=SIGN, subtr_hash=`26696', pos=[0, 1].
                 │     └──(hanger) #7, token=HANGER, subtr_hash=`4808', pos=[0, 1].
                 │           └──(base) #8, token=BASE, subtr_hash=`1160', pos=[0, 1].
                 │                 └──[normal`a'] #1, token=VAR, subtr_hash=`a', pos=[0, 1].
                 └──(pos) #9, token=SIGN, subtr_hash=`25732', pos=[2, 5].
                       └──(frac) #10, token=FRAC, subtr_hash=`57044', pos=[2, 5].
                             │──#1(hanger) #11, token=HANGER, subtr_hash=`4820', pos=[2, 3].
                             │     └──(base) #12, token=BASE, subtr_hash=`1164', pos=[2, 3].
                             │           └──[normal`b'] #2, token=VAR, subtr_hash=`b', pos=[2, 3].
                             └──#2(hanger) #13, token=HANGER, subtr_hash=`4832', pos=[4, 5].
                                   └──(base) #14, token=BASE, subtr_hash=`1168', pos=[4, 5].
                                         └──[normal`c'] #3, token=VAR, subtr_hash=`c', pos=[4, 5].

3 leaf-root paths
- [path#1, leaf#1] normal`a': VAR(#1)/BASE(#8)/HANGER(#7)/SIGN(#6)/ADD(#5)/GTLS(#4) (fp 3552)
- [path#2, leaf#2] normal`b': VAR(#2)/BASE(#12)/HANGER(#11)/rank1(#0)/FRAC(#10)/SIGN(#9)/ADD(#5)/GTLS(#4) (fp 0552)
- [path#3, leaf#3] normal`c': VAR(#3)/BASE(#14)/HANGER(#13)/rank2(#0)/FRAC(#10)/SIGN(#9)/ADD(#5)/GTLS(#4) (fp 0552)
```

You can find the interface `tex_parse()` at `tex-parser/tex-parser.h`
```c
struct tex_parse_ret {
    uint32_t         code;
    char             msg[MAX_PARSER_ERR_STR];
    struct subpaths  lrpaths;
    void            *operator_tree;
};

struct tex_parse_ret tex_parse(const char *); 
```

### Math Index
The `math_index_add()` interface at `math-index-v3/math-index.h`
```c
size_t math_index_add(math_index_t, doc_id_t docID, exp_id_t expID, struct subpaths);
```
will take docID, expID and parser generated leaf-root paths (a subset of subpaths) and generate a *subpath set* which
consists partial bottom-up leaf-to-internal-node paths (or *prefix paths*).

Here is the pseudo C code showing our inverted list item structure
```c
/* math inverted list items */
struct math_invlist_item {
	/* 8-byte global key */
	uint32_t docID; /* 4 bytes */
	union {
		uint32_t secID;
		struct {
			uint16_t sect_root;
			uint16_t expID;
		};
	}; /* 4 bytes */

	uint8_t  sect_width;
	uint8_t  orig_width;
	/* padding 16 bits here */
	uint32_t symbinfo_offset; /* pointing to symbinfo file offset */
	/* 4 bytes */
}; /* 4 x 4 = 16 bytes in total */

#define MAX_INDEX_EXP_SYMBOL_SPLITS 8

struct symbsplt {
	uint16_t symbol;
	uint8_t  splt_w;
};

struct symbinfo {
	uint32_t ophash:24;
	uint32_t n_splits:8;

	struct symbsplt split[MAX_INDEX_EXP_SYMBOL_SPLITS];
};
```

(more to be written here...)


### Papers
Some academic papers/posters describe in detail what our search
methods are. You may find useful to read these resources:

1. [ECIR16 Slides](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-OPMES-slides-handouts.pdf)
2. [ECIR16 Poster](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-Wei-Poster-publish.pdf)
3. [ECIR16 Demo](https://github.com/tkhost/tkhost.github.io/blob/master/opmes/ecir2016.pdf)
4. [Master thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf)
5. [ECIR19 Paper - Structure search model](https://ecir2019.org/accepted-papers/)
6. [ECIR20 Paper - Formula query efficiency](https://drive.google.com/open?id=1QjKVpgsTAIMLqrIDhdDOHvDa7sLvoxq7)
