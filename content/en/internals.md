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

The following is an example output for expression `$a + a + b/c=$` (notice the RHS has nothing so it will reduce into *nil*)
```
Operator tree:
     └──(equal) #5, token=GTLS, subtr_hash=`34760', pos=[0, 11].
           └──(plus) #6, token=ADD, subtr_hash=`10348', pos=[0, 11].
                 │──(pos) #7, token=SIGN, subtr_hash=`26696', pos=[0, 1].
                 │     └──(hanger) #8, token=HANGER, subtr_hash=`4808', pos=[0, 1].
                 │           └──(base) #9, token=BASE, subtr_hash=`1160', pos=[0, 1].
                 │                 └──[normal`a'] #1, token=VAR, subtr_hash=`a', pos=[0, 1].
                 │──(pos) #10, token=SIGN, subtr_hash=`26696', pos=[4, 5].
                 │     └──(hanger) #11, token=HANGER, subtr_hash=`4808', pos=[4, 5].
                 │           └──(base) #12, token=BASE, subtr_hash=`1160', pos=[4, 5].
                 │                 └──[normal`a'] #2, token=VAR, subtr_hash=`a', pos=[4, 5].
                 └──(pos) #13, token=SIGN, subtr_hash=`25732', pos=[8, 11].
                       └──(frac) #14, token=FRAC, subtr_hash=`57044', pos=[8, 11].
                             │──#1(hanger) #15, token=HANGER, subtr_hash=`4820', pos=[8, 9].
                             │     └──(base) #16, token=BASE, subtr_hash=`1164', pos=[8, 9].
                             │           └──[normal`b'] #3, token=VAR, subtr_hash=`b', pos=[8, 9].
                             └──#2(hanger) #17, token=HANGER, subtr_hash=`4832', pos=[10, 11].
                                   └──(base) #18, token=BASE, subtr_hash=`1168', pos=[10, 11].
                                         └──[normal`c'] #4, token=VAR, subtr_hash=`c', pos=[10, 11].

4 leaf-root paths
- [path#1, leaf#1] normal`a': VAR(#1)/BASE(#9)/HANGER(#8)/SIGN(#7)/ADD(#6)/GTLS(#5) (fp 3552)
- [path#2, leaf#2] normal`a': VAR(#2)/BASE(#12)/HANGER(#11)/SIGN(#10)/ADD(#6)/GTLS(#5) (fp 3552)
- [path#3, leaf#3] normal`b': VAR(#3)/BASE(#16)/HANGER(#15)/rank1(#0)/FRAC(#14)/SIGN(#13)/ADD(#6)/GTLS(#5) (fp 0552)
- [path#4, leaf#4] normal`c': VAR(#4)/BASE(#18)/HANGER(#17)/rank2(#0)/FRAC(#14)/SIGN(#13)/ADD(#6)/GTLS(#5) (fp 0552)
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
(the word *subpath* refers to a full length leaf-root path or any paritial path)

### Math Index
The `math_index_add()` interface at `math-index-v3/math-index.h`
```c
size_t math_index_add(math_index_t, doc_id_t docID, exp_id_t expID, struct subpaths);
```
will take a specified docID, expID and parser generated leaf-root paths from a math formula,
to generate a *subpath set* which consists of all possible leaf-to-internal-node subpaths (or *prefix paths*)
from that subpath set, and group them by their path token sequence.
A multiple prefix paths falling into same group are called to contain *duplicates*.

An example subpath set generated from above example leaf-root paths:
```
subpath set (size=13)
[  0] prefix/VAR/BASE (3 duplicates: r9~l1 r12~l2 r16~l3 r18~l4 )
         qnode#9/1-0003{ normal`a'/1 0x1 } 
         qnode#12/1-0003{ normal`a'/1 0x2 } 
         qnode#16/1-0003{ normal`b'/1 0x4 } 
         qnode#18/1-0003{ normal`c'/1 0x8 } 
[  1] prefix/VAR/BASE/HANGER (3 duplicates: r8~l1 r11~l2 r15~l3 r17~l4 )
         qnode#8/1-0035{ normal`a'/1 0x1 } 
         qnode#11/1-0035{ normal`a'/1 0x2 } 
         qnode#15/1-0030{ normal`b'/1 0x4 } 
         qnode#17/1-0030{ normal`c'/1 0x8 } 
[  2] prefix/VAR/BASE/HANGER/SIGN (1 duplicates: r7~l1 r10~l2 )
         qnode#7/1-0355{ normal`a'/1 0x1 } 
         qnode#10/1-0355{ normal`a'/1 0x2 } 
[  3] prefix/VAR/BASE/HANGER/SIGN/ADD (1 duplicates: r6~l1 r6~l2 )
         qnode#6/2-3552{ normal`a'/2 0x3 } 
[  4] prefix/VAR/BASE/HANGER/rank1/FRAC (0 duplicates: r14~l3 )
         qnode#14/1-3055{ normal`b'/1 0x4 } 
[  5] prefix/VAR/BASE/HANGER/rank2/FRAC (0 duplicates: r14~l4 )
         qnode#14/1-3055{ normal`c'/1 0x8 } 
[  6] prefix/VAR/BASE/HANGER/SIGN/ADD/GTLS (1 duplicates: r5~l1 r5~l2 )
         qnode#5/2-3552{ normal`a'/2 0x3 } 
[  7] prefix/VAR/BASE/HANGER/rank1/FRAC/SIGN (0 duplicates: r13~l3 )
         qnode#13/1-0552{ normal`b'/1 0x4 } 
[  8] prefix/VAR/BASE/HANGER/rank2/FRAC/SIGN (0 duplicates: r13~l4 )
         qnode#13/1-0552{ normal`c'/1 0x8 } 
[  9] prefix/VAR/BASE/HANGER/rank1/FRAC/SIGN/ADD (0 duplicates: r6~l3 )
         qnode#6/1-0552{ normal`b'/1 0x4 } 
[ 10] prefix/VAR/BASE/HANGER/rank2/FRAC/SIGN/ADD (0 duplicates: r6~l4 )
         qnode#6/1-0552{ normal`c'/1 0x8 } 
[ 11] prefix/VAR/BASE/HANGER/rank1/FRAC/SIGN/ADD/GTLS (0 duplicates: r5~l3 )
         qnode#5/1-0552{ normal`b'/1 0x4 } 
[ 12] prefix/VAR/BASE/HANGER/rank2/FRAC/SIGN/ADD/GTLS (0 duplicates: r5~l4 )
         qnode#5/1-0552{ normal`c'/1 0x8 } 
```

Here is the C code snippet defining the math inverted list item
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
